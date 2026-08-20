#!/usr/bin/env python3
"""Mine reviewable AI-style pattern candidates from labeled JSONL corpora.

The report contains recurring normalized spans and aggregate evidence only.
It never emits complete source documents or document identifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from copy import deepcopy
from collections import defaultdict
from pathlib import Path

from style_audit import SENTENCE_SPLIT, WORD


ALLOWED_LABELS = {"ai", "human", "mixed"}
MAX_DOCUMENTS = 5000
MAX_DOCUMENT_CHARACTERS = 50000
PRIVATE_SPAN = re.compile(
    r"https?://\S+|www\.\S+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|"
    r"\+?\d[\d\s().-]{6,}\d|"
    r'"[^"\n]{2,}"|“[^”\n]{2,}”|«[^»\n]{2,}»',
    re.I,
)


def normalized_tokens(text: str) -> list[str]:
    masked = PRIVATE_SPAN.sub(" ", text)
    return [
        token.casefold()
        for token in WORD.findall(masked)
        if not any(character.isdigit() for character in token)
    ]


def useful_span(tokens: tuple[str, ...]) -> bool:
    return bool(tokens) and any(len(token) >= 4 for token in tokens)


def ngrams(tokens: list[str], low: int = 2, high: int = 4) -> set[str]:
    values = set()
    for width in range(low, high + 1):
        for start in range(0, len(tokens) - width + 1):
            span = tuple(tokens[start : start + width])
            if useful_span(span):
                values.add(" ".join(span))
    return values


def opening_features(text: str, unit: str) -> set[str]:
    if unit == "sentence_opening":
        blocks = [part.strip() for part in SENTENCE_SPLIT.split(text) if part.strip()]
    else:
        blocks = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    values = set()
    for block in blocks:
        tokens = normalized_tokens(block)
        for width in range(2, min(4, len(tokens)) + 1):
            span = tuple(tokens[:width])
            if useful_span(span):
                values.add(" ".join(span))
    return values


def extract_features(text: str) -> set[tuple[str, str]]:
    tokens = normalized_tokens(text)
    features = {("ngram", value) for value in ngrams(tokens)}
    features.update(
        ("sentence_opening", value)
        for value in opening_features(text, "sentence_opening")
    )
    features.update(
        ("paragraph_opening", value)
        for value in opening_features(text, "paragraph_opening")
    )
    return features


def candidate_id(kind: str, value: str, language: str, channel: str) -> str:
    payload = "\0".join((kind, value, language, channel)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def validate_record(record: dict, line_number: int) -> dict:
    if not isinstance(record, dict):
        raise ValueError(f"line {line_number}: record must be an object")
    text = record.get("text")
    label = record.get("label")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"line {line_number}: text must be non-empty")
    if len(text) > MAX_DOCUMENT_CHARACTERS:
        raise ValueError(
            f"line {line_number}: text exceeds {MAX_DOCUMENT_CHARACTERS} characters"
        )
    if label not in ALLOWED_LABELS:
        raise ValueError(
            f"line {line_number}: label must be one of {sorted(ALLOWED_LABELS)}"
        )
    return {
        "text": text,
        "label": label,
        "language": str(record.get("language", "unknown")).casefold(),
        "channel": str(record.get("channel", "unknown")).casefold(),
        "source": str(record.get("source", "unknown")).casefold(),
        "topic": str(record.get("topic", "unknown")).casefold(),
    }


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"line {line_number}: invalid JSON: {error.msg}") from error
        records.append(validate_record(raw, line_number))
        if len(records) > MAX_DOCUMENTS:
            raise ValueError(f"corpus exceeds {MAX_DOCUMENTS} documents")
    if not records:
        raise ValueError("corpus is empty")
    return records


def mine_records(
    records: list[dict],
    *,
    language: str | None = None,
    channel: str | None = None,
    min_ai_docs: int = 3,
    min_ai_rate: float = 0.25,
    max_human_rate: float = 0.1,
    min_lift: float = 3.0,
    min_ai_sources: int = 2,
    max_candidates: int = 100,
) -> dict:
    language_filter = language.casefold() if language else None
    channel_filter = channel.casefold() if channel else None
    selected = [
        record
        for record in records
        if (language_filter is None or record["language"] == language_filter)
        and (channel_filter is None or record["channel"] == channel_filter)
    ]
    ai_records = [record for record in selected if record["label"] == "ai"]
    human_records = [record for record in selected if record["label"] == "human"]
    mixed_records = [record for record in selected if record["label"] == "mixed"]
    if not ai_records or not human_records:
        raise ValueError("mining requires both ai and human records")

    ai_docs: dict[tuple[str, str], set[int]] = defaultdict(set)
    human_docs: dict[tuple[str, str], set[int]] = defaultdict(set)
    ai_sources: dict[tuple[str, str], set[str]] = defaultdict(set)

    for index, record in enumerate(ai_records):
        for feature in extract_features(record["text"]):
            ai_docs[feature].add(index)
            ai_sources[feature].add(record["source"])
    for index, record in enumerate(human_records):
        for feature in extract_features(record["text"]):
            human_docs[feature].add(index)

    candidates = []
    smoothing = 1.0 / max(len(ai_records) + len(human_records), 1)
    output_language = language_filter or "mixed"
    output_channel = channel_filter or "mixed"
    for feature, ai_indexes in ai_docs.items():
        kind, value = feature
        ai_count = len(ai_indexes)
        human_count = len(human_docs.get(feature, set()))
        ai_rate = ai_count / len(ai_records)
        human_rate = human_count / len(human_records)
        lift = (ai_rate + smoothing) / (human_rate + smoothing)
        source_count = len(ai_sources[feature])
        if ai_count < min_ai_docs:
            continue
        if ai_rate < min_ai_rate or human_rate > max_human_rate:
            continue
        if lift < min_lift or source_count < min_ai_sources:
            continue
        contrast = ai_rate - human_rate
        score = contrast * math.log2(1.0 + lift) * math.log2(1.0 + ai_count)
        candidates.append(
            {
                "id": candidate_id(
                    kind, value, output_language, output_channel
                ),
                "kind": kind,
                "language": output_language,
                "channel": output_channel,
                "scope": "universal_candidate",
                "value": value,
                "score": round(score, 4),
                "evidence": {
                    "ai_documents": ai_count,
                    "human_documents": human_count,
                    "ai_document_rate": round(ai_rate, 4),
                    "human_document_rate": round(human_rate, 4),
                    "ai_sources": source_count,
                    "lift": round(lift, 3),
                },
                "status": "candidate",
            }
        )

    candidates.sort(
        key=lambda item: (
            item["score"],
            item["evidence"]["ai_documents"],
            len(item["value"]),
        ),
        reverse=True,
    )
    kind_priority = {"paragraph_opening": 3, "sentence_opening": 2, "ngram": 1}
    exact_values: dict[str, dict] = {}
    for item in candidates:
        existing = exact_values.get(item["value"])
        if existing is None or kind_priority[item["kind"]] > kind_priority[existing["kind"]]:
            exact_values[item["value"]] = item
    candidates = sorted(
        exact_values.values(),
        key=lambda item: (
            item["score"],
            item["evidence"]["ai_documents"],
            len(item["value"]),
            kind_priority[item["kind"]],
        ),
        reverse=True,
    )
    consolidated = []
    for item in candidates:
        redundant = any(
            item["kind"] == selected_item["kind"]
            and item["value"] in selected_item["value"]
            and item["evidence"] == selected_item["evidence"]
            for selected_item in consolidated
        )
        if not redundant:
            consolidated.append(item)
    candidates = consolidated

    warnings = []
    if len(ai_records) < 10 or len(human_records) < 10:
        warnings.append("exploratory_only_small_corpus")
    if len({record["source"] for record in ai_records}) < 2:
        warnings.append("single_ai_source_family")
    if language_filter is None:
        warnings.append("mixed_language_mining_can_create_spurious_patterns")
    if channel_filter is None:
        warnings.append("mixed_channel_mining_can_create_spurious_patterns")
    ai_topics = {
        record["topic"] for record in ai_records if record.get("topic") != "unknown"
    }
    human_topics = {
        record["topic"]
        for record in human_records
        if record.get("topic") != "unknown"
    }
    if ai_topics and human_topics and not ai_topics.intersection(human_topics):
        warnings.append("ai_and_human_topic_controls_do_not_overlap")

    return {
        "notice": (
            "Candidate mining only. Validate on held-out human and AI texts "
            "before promoting any pattern."
        ),
        "corpus": {
            "selected_documents": len(selected),
            "ai_documents": len(ai_records),
            "human_documents": len(human_records),
            "mixed_documents": len(mixed_records),
            "ai_sources": len({record["source"] for record in ai_records}),
            "known_ai_topics": len(ai_topics),
            "known_human_topics": len(human_topics),
            "language": output_language,
            "channel": output_channel,
        },
        "config": {
            "min_ai_docs": min_ai_docs,
            "min_ai_rate": min_ai_rate,
            "max_human_rate": max_human_rate,
            "min_lift": min_lift,
            "min_ai_sources": min_ai_sources,
            "max_candidates": max_candidates,
        },
        "warnings": warnings,
        "candidates": candidates[:max_candidates],
    }


def validate_candidates(
    report: dict,
    records: list[dict],
    *,
    language: str | None = None,
    channel: str | None = None,
    min_ai_docs: int = 2,
    min_ai_rate: float = 0.2,
    max_human_rate: float = 0.05,
) -> dict:
    language_filter = language.casefold() if language else None
    channel_filter = channel.casefold() if channel else None
    selected = [
        record
        for record in records
        if (language_filter is None or record["language"] == language_filter)
        and (channel_filter is None or record["channel"] == channel_filter)
    ]
    ai_records = [record for record in selected if record["label"] == "ai"]
    human_records = [record for record in selected if record["label"] == "human"]
    if not ai_records or not human_records:
        raise ValueError("validation requires both ai and human records")

    ai_features = [extract_features(record["text"]) for record in ai_records]
    human_features = [extract_features(record["text"]) for record in human_records]
    validated = deepcopy(report)
    training_corpus = validated.get("corpus", {})
    blocking_training_warnings = {
        "exploratory_only_small_corpus",
        "single_ai_source_family",
        "ai_and_human_topic_controls_do_not_overlap",
    }
    training_ready = (
        training_corpus.get("ai_documents", 0) >= 10
        and training_corpus.get("human_documents", 0) >= 10
        and not blocking_training_warnings.intersection(
            validated.get("warnings", [])
        )
    )
    passed = 0
    for candidate in validated.get("candidates", []):
        feature = (candidate["kind"], candidate["value"])
        ai_hits = sum(feature in features for features in ai_features)
        human_hits = sum(feature in features for features in human_features)
        ai_rate = ai_hits / len(ai_records)
        human_rate = human_hits / len(human_records)
        promotion_ready = (
            training_ready
            and len(ai_records) >= 10
            and len(human_records) >= 10
            and ai_hits >= min_ai_docs
            and ai_rate >= min_ai_rate
            and human_rate <= max_human_rate
        )
        candidate["validation"] = {
            "ai_documents": ai_hits,
            "human_documents": human_hits,
            "ai_document_rate": round(ai_rate, 4),
            "human_document_rate": round(human_rate, 4),
            "promotion_ready": promotion_ready,
        }
        candidate["status"] = "validated" if promotion_ready else "rejected"
        passed += int(promotion_ready)
    validated["validation"] = {
        "held_out_documents": len(selected),
        "ai_documents": len(ai_records),
        "human_documents": len(human_records),
        "language": language_filter or "mixed",
        "channel": channel_filter or "mixed",
        "min_ai_docs": min_ai_docs,
        "min_ai_rate": min_ai_rate,
        "max_human_rate": max_human_rate,
        "training_corpus_ready": training_ready,
        "promotion_ready_candidates": passed,
    }
    return validated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="UTF-8 JSONL corpus")
    parser.add_argument("--language")
    parser.add_argument("--channel")
    parser.add_argument("--min-ai-docs", type=int, default=3)
    parser.add_argument("--min-ai-rate", type=float, default=0.25)
    parser.add_argument("--max-human-rate", type=float, default=0.1)
    parser.add_argument("--min-lift", type=float, default=3.0)
    parser.add_argument("--min-ai-sources", type=int, default=2)
    parser.add_argument("--max-candidates", type=int, default=100)
    parser.add_argument(
        "--validation-file",
        help="Optional held-out JSONL corpus used only to validate mined candidates",
    )
    parser.add_argument("--validation-min-ai-docs", type=int, default=2)
    parser.add_argument("--validation-min-ai-rate", type=float, default=0.2)
    parser.add_argument("--validation-max-human-rate", type=float, default=0.05)
    parser.add_argument("--output", help="Write JSON report; omit for stdout")
    args = parser.parse_args()
    try:
        records = load_jsonl(Path(args.file))
        result = mine_records(
            records,
            language=args.language,
            channel=args.channel,
            min_ai_docs=max(args.min_ai_docs, 1),
            min_ai_rate=max(0.0, min(args.min_ai_rate, 1.0)),
            max_human_rate=max(0.0, min(args.max_human_rate, 1.0)),
            min_lift=max(args.min_lift, 1.0),
            min_ai_sources=max(args.min_ai_sources, 1),
            max_candidates=max(args.max_candidates, 1),
        )
        if args.validation_file:
            validation_records = load_jsonl(Path(args.validation_file))
            result = validate_candidates(
                result,
                validation_records,
                language=args.language,
                channel=args.channel,
                min_ai_docs=max(args.validation_min_ai_docs, 1),
                min_ai_rate=max(
                    0.0, min(args.validation_min_ai_rate, 1.0)
                ),
                max_human_rate=max(
                    0.0, min(args.validation_max_human_rate, 1.0)
                ),
            )
    except (OSError, TypeError, ValueError) as error:
        parser.error(str(error))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
