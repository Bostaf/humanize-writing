#!/usr/bin/env python3
"""Heuristic prose style audit.

This is a quality diagnostic, not an AI-authorship detector.
Metric selection incorporates ideas from Aboudjem/humanizer-skill (MIT);
the multilingual implementation and interpretation rules are local.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path


DEFAULT_ADAPTIVE_CATALOG = (
    Path(__file__).resolve().parent.parent / "references" / "adaptive-patterns.json"
)


MARKERS = {
    "generic_opening": [
        r"\bin today'?s (?:rapidly changing|fast-paced|digital|modern) world\b",
        r"\bin the (?:ever-evolving|dynamic) landscape\b",
        r"\bу сучасному світі\b",
        r"\bв епоху стрімких змін\b",
        r"\bв современном мире\b",
    ],
    "inflated_significance": [
        r"\b(?:pivotal|transformative|groundbreaking|game-changing)\b",
        r"\b(?:a testament to|cannot be overstated|plays a vital role)\b",
        r"\b(?:трансформаційн\w+|важко переоцінити|відігра\w+ ключову роль)\b",
        r"\b(?:трансформационн\w+|трудно переоценить|игра\w+ ключевую роль)\b",
    ],
    "stock_ai_lexicon": [
        r"\b(?:delve|foster|leverage|navigate|unlock|harness)\b",
        r"\b(?:robust|seamless|comprehensive|cutting-edge)\b",
        r"\b(?:underscores?|showcases?|ever-evolving|tapestry)\b",
        r"\b(?:безшовн\w+|комплексн\w+ підхід|підкреслює важливість)\b",
        r"\b(?:бесшовн\w+|комплексн\w+ подход|подчеркивает важность)\b",
    ],
    "empty_signposting": [
        r"\b(?:it is (?:important|worth noting) (?:to note )?that)\b",
        r"\b(?:moreover|furthermore|additionally|ultimately)\b",
        r"\b(?:варто зазначити|важливо розуміти|крім того)\b",
        r"\b(?:стоит отметить|важно понимать|кроме того)\b",
    ],
    "mirrored_contrast": [
        r"\bnot (?:just|only)\b.{0,100}\bbut (?:also )?\b",
        r"\brather than merely\b",
        r"\bне (?:просто|лише)\b.{0,100}\bа (?:й|також)?\b",
        r"\bне (?:просто|только)\b.{0,100}\bа (?:и|также)?\b",
    ],
    "participial_afterthought": [
        r",\s+(?:enabling|ensuring|highlighting|underscoring|showcasing)\b",
        r",\s+(?:забезпечуючи|дозволяючи|підкреслюючи)\b",
        r",\s+(?:обеспечивая|позволяя|подчеркивая)\b",
    ],
    "vague_attribution": [
        r"\b(?:experts|researchers|industry leaders) (?:say|believe|suggest)\b",
        r"\b(?:research|studies) (?:shows?|suggests?|indicates?)\b",
        r"\b(?:експерти|дослідники) (?:вважають|кажуть|зазначають)\b",
        r"\b(?:эксперты|исследователи) (?:считают|говорят|отмечают)\b",
    ],
    "assistant_artifact": [
        r"\b(?:of course|certainly|great question|you'?re absolutely right)\b",
        r"\b(?:i hope this helps|let me know if|would you like me to)\b",
        r"\b(?:here is an overview|let me walk you through|here'?s what you need to know)\b",
        r"\b(?:звісно|чудове питання|сподіваюся, це допоможе)\b",
        r"\b(?:конечно|отличный вопрос|надеюсь, это поможет)\b",
    ],
    "theatrical_hook": [
        r"(?:^|[.!?]\s+)(?:the catch|the kicker|the brutal truth|sound familiar)\?",
        r"(?:^|[.!?]\s+)here'?s the thing[.:]",
        r"(?:^|[.!?]\s+)(?:у чому підступ|жорстока правда)\?",
        r"(?:^|[.!?]\s+)(?:в чём подвох|жестокая правда)\?",
    ],
    "aphorism_formula": [
        r"\b\w+ is the (?:currency|language|architecture) of \w+\b",
        r"\b\w+ is where \w+ meets \w+\b",
        r"\b\w+ is the new \w+\b",
        r"\b\w+ (?:це|—) (?:валюта|мова|архітектура) \w+\b",
        r"\b\w+ (?:это|—) (?:валюта|язык|архитектура) \w+\b",
    ],
    "diff_anchored": [
        r"\b(?:was added to|now uses|has been updated to|replaces the old|previously used)\b",
        r"\b(?:було додано|тепер використовує|оновлено для|замінює старий)\b",
        r"\b(?:было добавлено|теперь использует|обновлено для|заменяет старый)\b",
    ],
    "false_agency": [
        r"\b(?:the data tells us|the market rewards|the decision emerges)\b",
        r"\b(?:дані говорять нам|ринок винагороджує|рішення виникає)\b",
        r"\b(?:данные говорят нам|рынок вознаграждает|решение возникает)\b",
    ],
    "reasoning_artifact": [
        r"\b(?:let me think|breaking this down|first, i'?ll|step 1:)\b",
        r"\b(?:давайте подумаю|розберімо це|крок 1:)\b",
        r"\b(?:давайте подумаем|разберём это|шаг 1:)\b",
    ],
    "generic_summary": [
        r"(?:^|[.!?]\s+)(?:in conclusion|in summary|to sum up|overall),",
        r"(?:^|[.!?]\s+)(?:на завершення|підсумовуючи|загалом),",
        r"(?:^|[.!?]\s+)(?:в заключение|подводя итог|в целом),",
    ],
}

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[^\W\d_])", re.UNICODE)
WORD = re.compile(r"[\w’'-]+", re.UNICODE)
SUSPICIOUS_UNICODE = re.compile(r"[\u00ad\u200b\u200c\u200d\u2060\ufeff]")
PARAGRAPH_STAGE_STARTS = [
    re.compile(
        r"^(?:therefore|for (?:important|high-stakes|public) (?:work|cases|materials)|"
        r"as a result|the goal is|the main goal|to do this|that is why)\b",
        re.I,
    ),
    re.compile(
        r"^(?:тому(?: я| ми)?|для (?:важливих|публічних) (?:матеріалів|текстів)|"
        r"у результаті|в основу(?: я| ми)?|основна мета|мета проста|саме тому)\b",
        re.I,
    ),
    re.compile(
        r"^(?:поэтому(?: я| мы)?|для (?:важных|публичных) (?:материалов|текстов)|"
        r"в результате|за основу(?: я| мы)?|основная цель|цель простая|именно поэтому)\b",
        re.I,
    ),
]


def mask_protected(text: str) -> str:
    """Mask code, blockquotes, and URLs while preserving approximate boundaries."""

    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"(?m)^(?: {4}|\t).*$", " ", text)
    text = re.sub(r"`[^`\n]+`", " ", text)
    text = re.sub(r"(?m)^>\s?.*$", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    return text


def coefficient_of_variation(values: list[int]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance) / mean


def mattr(words: list[str], window: int = 50) -> float:
    """Return moving-average type-token ratio.

    MATTR is more comparable across texts of different lengths than raw TTR.
    For short texts, use the whole available sequence.
    """

    if not words:
        return 0.0
    width = min(window, len(words))
    ratios = [
        len(set(words[start : start + width])) / width
        for start in range(0, len(words) - width + 1)
    ]
    return sum(ratios) / len(ratios)


def goh_barabasi_burstiness(values: list[int]) -> float:
    """Return (standard deviation - mean) / (standard deviation + mean)."""

    if not values:
        return 0.0
    mean = statistics.fmean(values)
    deviation = statistics.pstdev(values)
    denominator = deviation + mean
    return (deviation - mean) / denominator if denominator else 0.0


def unicode_findings(text: str) -> list[dict]:
    """Report invisible or formatting code points without modifying the text."""

    findings = []
    for index, char in enumerate(text):
        if SUSPICIOUS_UNICODE.fullmatch(char):
            findings.append(
                {
                    "index": index,
                    "codepoint": f"U+{ord(char):04X}",
                    "name": unicodedata.name(char, "UNKNOWN"),
                }
            )
    return findings[:20]


def longest_uniform_run(values: list[int]) -> int:
    """Return longest run whose adjacent lengths differ by at most 3 words."""

    if not values:
        return 0
    longest = current = 1
    for previous, current_value in zip(values, values[1:]):
        if abs(current_value - previous) <= 3:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def trigram_repetition_rate(words: list[str]) -> float:
    if len(words) < 3:
        return 0.0
    trigrams = list(zip(words, words[1:], words[2:]))
    repeated = sum(count - 1 for count in Counter(trigrams).values() if count > 1)
    return repeated / len(trigrams)


def staged_paragraph_starts(paragraphs: list[str]) -> list[str]:
    """Return later paragraph openings that explicitly announce their function."""

    matches = []
    for paragraph in paragraphs[1:]:
        normalized = re.sub(r"\s+", " ", paragraph.strip())
        for pattern in PARAGRAPH_STAGE_STARTS:
            match = pattern.search(normalized)
            if match:
                matches.append(match.group(0))
                break
    return matches


def load_adaptive_patterns(path: Path | None = None) -> tuple[list[dict], dict]:
    catalog_path = path or DEFAULT_ADAPTIVE_CATALOG
    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        patterns = payload.get("patterns", [])
        if not isinstance(patterns, list):
            raise ValueError("'patterns' must be a list")
        active = [
            item
            for item in patterns
            if isinstance(item, dict)
            and item.get("status") == "active"
            and item.get("scope") == "universal"
            and item.get("kind") in {"ngram", "sentence_opening", "paragraph_opening"}
            and isinstance(item.get("value"), str)
            and item["value"].strip()
        ]
        return active, {
            "status": "loaded",
            "version": payload.get("version"),
            "active_patterns": len(active),
            "catalog": catalog_path.name,
        }
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        return [], {
            "status": "error",
            "active_patterns": 0,
            "catalog": catalog_path.name,
            "error": str(error),
        }


def adaptive_findings(
    normalized: str,
    sentences: list[str],
    paragraphs: list[str],
    patterns: list[dict],
) -> list[dict]:
    grouped: dict[str, list[str]] = {}
    folded_text = normalized.casefold()
    folded_sentences = [sentence.casefold() for sentence in sentences]
    folded_paragraphs = [paragraph.casefold() for paragraph in paragraphs]
    for item in patterns:
        if item.get("status", "active") != "active":
            continue
        if item.get("scope", "universal") != "universal":
            continue
        value = item["value"].strip().casefold()
        kind = item["kind"]
        if kind == "ngram":
            matched = bool(
                re.search(rf"(?<!\w){re.escape(value)}(?!\w)", folded_text)
            )
        elif kind == "sentence_opening":
            matched = any(sentence.startswith(value) for sentence in folded_sentences)
        else:
            matched = any(paragraph.startswith(value) for paragraph in folded_paragraphs)
        if matched:
            grouped.setdefault(f"adaptive_{kind}", []).append(value)
    return [
        {
            "category": category,
            "count": len(values),
            "examples": list(dict.fromkeys(values))[:5],
        }
        for category, values in grouped.items()
    ]


def audit(
    text: str,
    include_protected: bool = False,
    adaptive_patterns: list[dict] | None = None,
    adaptive_catalog_path: Path | None = None,
) -> dict:
    suspicious_unicode = unicode_findings(text)
    suspicious_unicode_count = len(SUSPICIOUS_UNICODE.findall(text))
    if not include_protected:
        text = mask_protected(text)
    normalized = re.sub(r"[ \t]+", " ", text.strip())
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(normalized) if s.strip()]
    if not sentences and normalized:
        sentences = [normalized]
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    words = WORD.findall(normalized)
    lowercase_words = [word.lower() for word in words]
    sentence_lengths = [len(WORD.findall(sentence)) for sentence in sentences]
    paragraph_lengths = [len(WORD.findall(paragraph)) for paragraph in paragraphs]
    staged_starts = staged_paragraph_starts(paragraphs)

    starts = []
    for sentence in sentences:
        sentence_words = [word.lower() for word in WORD.findall(sentence)]
        if sentence_words:
            starts.append(" ".join(sentence_words[: min(2, len(sentence_words))]))
    repeated_starts = [
        {"start": start, "count": count}
        for start, count in Counter(starts).most_common()
        if count >= 2
    ][:8]

    findings = []
    lower = normalized.lower()
    for category, patterns in MARKERS.items():
        matches = []
        for pattern in patterns:
            matches.extend(match.group(0) for match in re.finditer(pattern, lower, re.I))
        if matches:
            findings.append(
                {
                    "category": category,
                    "count": len(matches),
                    "examples": list(dict.fromkeys(matches))[:5],
                }
            )

    if adaptive_patterns is None:
        adaptive_patterns, adaptive_meta = load_adaptive_patterns(
            adaptive_catalog_path
        )
    else:
        adaptive_meta = {
            "status": "provided",
            "version": None,
            "active_patterns": len(adaptive_patterns),
            "catalog": None,
        }
    findings.extend(
        adaptive_findings(normalized, sentences, paragraphs, adaptive_patterns)
    )

    later_paragraphs = max(len(paragraphs) - 1, 0)
    staged_ratio = len(staged_starts) / later_paragraphs if later_paragraphs else 0.0
    if len(staged_starts) >= 2 and staged_ratio >= 0.6:
        findings.append(
            {
                "category": "staged_paragraph_progression",
                "count": len(staged_starts),
                "examples": list(dict.fromkeys(staged_starts))[:5],
            }
        )

    paragraph_cv = coefficient_of_variation(paragraph_lengths)
    if len(paragraphs) >= 3 and len(words) >= 80 and paragraph_cv <= 0.12:
        findings.append(
            {
                "category": "uniform_paragraph_structure",
                "count": 1,
                "examples": [
                    "paragraph lengths are unusually uniform for this short text"
                ],
            }
        )

    punctuation = {
        "em_dashes": normalized.count("—"),
        "semicolons": normalized.count(";"),
        "parenthetical_pairs": min(normalized.count("("), normalized.count(")")),
        "colons": normalized.count(":"),
    }

    signals = sum(item["count"] for item in findings)
    repeated_penalty = sum(item["count"] - 1 for item in repeated_starts)
    density = round((signals + repeated_penalty) * 100 / max(len(words), 1), 2)

    return {
        "notice": "Heuristic writing-quality audit; not an AI-authorship detector.",
        "metrics": {
            "words": len(words),
            "sentences": len(sentences),
            "paragraphs": len(paragraphs),
            "average_sentence_words": round(
                sum(sentence_lengths) / max(len(sentence_lengths), 1), 2
            ),
            "sentence_length_cv": round(coefficient_of_variation(sentence_lengths), 3),
            "sentence_length_stdev": round(
                statistics.pstdev(sentence_lengths) if sentence_lengths else 0.0, 3
            ),
            "sentence_length_burstiness": round(
                goh_barabasi_burstiness(sentence_lengths), 3
            ),
            "paragraph_length_cv": round(paragraph_cv, 3),
            "staged_paragraph_start_ratio": round(staged_ratio, 3),
            "longest_uniform_sentence_run": longest_uniform_run(sentence_lengths),
            "type_token_ratio": round(
                len(set(lowercase_words)) / max(len(lowercase_words), 1), 3
            ),
            "mattr_50": round(mattr(lowercase_words, 50), 3),
            "trigram_repetition_rate": round(
                trigram_repetition_rate(lowercase_words), 3
            ),
            "marker_density_per_100_words": density,
        },
        "punctuation": punctuation,
        "suspicious_unicode_characters": suspicious_unicode_count,
        "suspicious_unicode": suspicious_unicode,
        "repeated_sentence_starts": repeated_starts,
        "findings": findings,
        "adaptive_catalog": adaptive_meta,
    }


def render_text(result: dict) -> str:
    metrics = result["metrics"]
    lines = [
        result["notice"],
        "",
        f"Words: {metrics['words']}",
        f"Sentences: {metrics['sentences']}",
        f"Paragraphs: {metrics['paragraphs']}",
        f"Average sentence length: {metrics['average_sentence_words']} words",
        f"Sentence-length variation (CV): {metrics['sentence_length_cv']}",
        f"Sentence-length standard deviation: {metrics['sentence_length_stdev']}",
        f"Sentence-length burstiness: {metrics['sentence_length_burstiness']}",
        f"Paragraph-length variation (CV): {metrics['paragraph_length_cv']}",
        f"Staged paragraph-start ratio: {metrics['staged_paragraph_start_ratio']}",
        f"Longest uniform sentence run: {metrics['longest_uniform_sentence_run']}",
        f"Type-token ratio: {metrics['type_token_ratio']}",
        f"MATTR (50-word window): {metrics['mattr_50']}",
        f"Trigram repetition rate: {metrics['trigram_repetition_rate']}",
        f"Marker density: {metrics['marker_density_per_100_words']} per 100 words",
        f"Em dashes: {result['punctuation']['em_dashes']}",
        f"Suspicious Unicode characters: {result['suspicious_unicode_characters']}",
    ]
    if result["repeated_sentence_starts"]:
        lines.extend(["", "Repeated sentence starts:"])
        for item in result["repeated_sentence_starts"]:
            lines.append(f"- {item['start']!r}: {item['count']}")
    if result["findings"]:
        lines.extend(["", "Pattern findings:"])
        for item in result["findings"]:
            examples = ", ".join(repr(example) for example in item["examples"])
            lines.append(f"- {item['category']}: {item['count']} ({examples})")
    else:
        lines.extend(["", "No configured stock patterns found."])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="UTF-8 text file; omit to read stdin")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--include-protected",
        action="store_true",
        help="Include code, blockquotes, and URLs in pattern analysis",
    )
    parser.add_argument(
        "--adaptive-catalog",
        help="Optional adaptive-pattern catalog JSON; defaults to the bundled catalog",
    )
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        parser.error("input text is empty")

    result = audit(
        text,
        include_protected=args.include_protected,
        adaptive_catalog_path=Path(args.adaptive_catalog)
        if args.adaptive_catalog
        else None,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
