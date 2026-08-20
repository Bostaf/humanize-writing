#!/usr/bin/env python3
"""Rank rewrite candidates with fidelity-first, transparent quality gates.

Input is JSON from a file or stdin. Detector scores are optional and have a
small, capped influence; they can never override a failed fidelity gate.
The architecture synthesizes trajectory, hard-gate, pairwise-evaluation, and
diversity-control ideas documented in references/source-manifest.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from style_audit import WORD, audit


URL = re.compile(r"https?://[^\s)>}\]]+|www\.[^\s)>}\]]+", re.I)
NUMBER = re.compile(
    r"(?<![\w])(?:[$€£₴]\s*)?-?\d+(?:[.,]\d+)*(?:\s*[%‰]|(?:\s*[A-Za-zА-Яа-яІіЇїЄєҐґ]{1,5}))?(?![\w])"
)
INLINE_CODE = re.compile(r"`[^`\n]+`")
QUOTED = re.compile(r"""(?:"[^"\n]{2,}"|“[^”\n]{2,}”|«[^»\n]{2,}»)""")


def clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def words(text: str) -> list[str]:
    return [word.casefold() for word in WORD.findall(text)]


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return set(zip(*(tokens[offset:] for offset in range(n)))) if len(tokens) >= n else set()


def jaccard(left: set, right: set) -> float:
    if not left and not right:
        return 1.0
    return len(left & right) / max(len(left | right), 1)


def change_metrics(original: str, candidate: str) -> dict:
    source_words = words(original)
    candidate_words = words(candidate)
    lexical_change = 1.0 - jaccard(set(source_words), set(candidate_words))
    structural_change = 1.0 - jaccard(ngrams(source_words, 3), ngrams(candidate_words, 3))
    return {
        "lexical_change": round(lexical_change, 3),
        "structural_change": round(structural_change, 3),
        "length_ratio": round(len(candidate_words) / max(len(source_words), 1), 3),
    }


def extract_literals(text: str, include_quotes: bool = True) -> Counter:
    values = []
    for pattern in (URL, NUMBER, INLINE_CODE):
        values.extend(match.group(0) for match in pattern.finditer(text))
    if include_quotes:
        values.extend(match.group(0) for match in QUOTED.finditer(text))
    return Counter(values)


def literal_diff(required: Counter, actual: Counter) -> tuple[list[str], list[str]]:
    missing = list((required - actual).elements())
    added = list((actual - required).elements())
    return sorted(missing), sorted(added)


def normalized_external_score(candidate: dict, key: str, default: float) -> float:
    value = candidate.get(key)
    return default if value is None else clamp(value)


def distance_penalty(value: float, preferred: list[float]) -> float:
    low, high = preferred
    if low <= value <= high:
        return 0.0
    distance = low - value if value < low else value - high
    return min(distance, 1.0)


def evaluate_candidate(original: str, candidate: dict, config: dict) -> dict:
    text = candidate.get("text", "")
    candidate_id = str(candidate.get("id", "candidate"))
    include_quotes = bool(config.get("protect_quotes", True))
    required = extract_literals(original, include_quotes=include_quotes)
    actual = extract_literals(text, include_quotes=include_quotes)
    missing, added = literal_diff(required, actual)
    manual_literals = [str(value) for value in config.get("required_literals", [])]
    missing_manual = [
        literal
        for literal in manual_literals
        if text.count(literal) < original.count(literal) or literal not in text
    ]
    missing.extend(missing_manual)
    missing = sorted(set(missing))
    style = audit(text)
    changes = change_metrics(original, text)

    semantic = candidate.get("semantic_score")
    semantic_value = None if semantic is None else clamp(semantic)
    author_grounding = normalized_external_score(
        candidate, "author_grounding_score", 0.5
    )
    voice = normalized_external_score(candidate, "voice_score", 0.5)
    quality = normalized_external_score(candidate, "quality_score", 0.5)
    detector = candidate.get("detector_score")
    detector_raw = None if detector is None else clamp(detector)
    detector_value = detector_raw
    if detector_value is not None and config.get("detector_direction") == "lower_is_better":
        detector_value = 1.0 - detector_value

    failures = []
    if not text.strip():
        failures.append("empty_text")
    if missing:
        failures.append("missing_protected_literals")
    if added and bool(config.get("reject_added_literals", True)):
        failures.append("added_numbers_urls_code_or_quotes")
    if style["suspicious_unicode_characters"]:
        failures.append("suspicious_unicode")
    if semantic_value is None and bool(config.get("require_semantic", False)):
        failures.append("semantic_score_required")
    if semantic_value is not None and semantic_value < float(config.get("min_semantic", 0.9)):
        failures.append("semantic_score_below_threshold")
    if (
        config.get("min_author_grounding") is not None
        and author_grounding < float(config["min_author_grounding"])
    ):
        failures.append("author_grounding_score_below_threshold")
    if config.get("min_voice") is not None and voice < float(config["min_voice"]):
        failures.append("voice_score_below_threshold")
    if config.get("min_quality") is not None and quality < float(config["min_quality"]):
        failures.append("quality_score_below_threshold")
    if bool(config.get("require_detector_score", False)) and detector_raw is None:
        failures.append("detector_score_required")

    marker_density = style["metrics"]["marker_density_per_100_words"]
    repetition = style["metrics"]["trigram_repetition_rate"]
    style_score = clamp(1.0 - marker_density / 8.0 - repetition)

    lexical_target = config.get("lexical_change_target", [0.12, 0.6])
    structural_target = config.get("structural_change_target", [0.18, 0.85])
    distance_cost = (
        distance_penalty(changes["lexical_change"], lexical_target)
        + distance_penalty(changes["structural_change"], structural_target)
    ) / 2

    fidelity = semantic_value if semantic_value is not None else (0.5 if not missing and not added else 0.0)
    score = (
        0.36 * fidelity
        + 0.18 * author_grounding
        + 0.20 * voice
        + 0.16 * quality
        + 0.08 * style_score
        - 0.08 * distance_cost
    )
    detector_weight = min(clamp(config.get("detector_weight", 0.02)), 0.1)
    if detector_value is not None:
        score += detector_weight * detector_value
    if failures:
        score = -1.0
    warnings = []
    if semantic_value is None:
        warnings.append("semantic_score_missing")
    if candidate.get("author_grounding_score") is None:
        warnings.append("author_grounding_score_missing")
    if candidate.get("voice_score") is None:
        warnings.append("voice_score_missing")
    if candidate.get("quality_score") is None:
        warnings.append("quality_score_missing")

    return {
        "id": candidate_id,
        "passed": not failures,
        "score": round(score, 4),
        "gate_failures": failures,
        "warnings": warnings,
        "protected_literals": {"missing": missing, "added": added},
        "external_scores": {
            "semantic": semantic_value,
            "author_grounding": author_grounding,
            "voice": voice,
            "quality": quality,
            "detector": detector_value,
            "detector_raw": detector_raw,
            "detector_selection": detector_value,
        },
        "derived_scores": {
            "style": round(style_score, 3),
            "distance_penalty": round(distance_cost, 3),
            "detector_weight": round(detector_weight, 3),
        },
        "change_metrics": changes,
        "style_audit": style,
        "text": text,
    }


def rank_payload(payload: dict) -> dict:
    original = payload.get("original", "")
    candidates = payload.get("candidates", [])
    config = payload.get("config", {})
    if not isinstance(original, str) or not original.strip():
        raise ValueError("'original' must be a non-empty string")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("'candidates' must be a non-empty list")

    results = [evaluate_candidate(original, item, config) for item in candidates]
    results.sort(key=lambda item: (item["passed"], item["score"]), reverse=True)
    winner = next((item["id"] for item in results if item["passed"]), None)
    return {
        "notice": (
            "Fidelity-first editorial ranking. Detector scores are optional, capped, "
            "and are not evidence of authorship."
        ),
        "winner": winner,
        "all_candidates_failed": winner is None,
        "ranking": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="JSON input; omit to read stdin")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()
    raw = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    try:
        result = rank_payload(json.loads(raw))
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
