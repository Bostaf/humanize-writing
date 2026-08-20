#!/usr/bin/env python3
"""Small deterministic regression checks for the bundled audit and ranker."""

import json
from pathlib import Path

from candidate_rank import rank_payload
from deft_rewrite import build_payload
from pattern_miner import mine_records, validate_candidates
from style_audit import audit


TEMPLATED_UKRAINIAN = """
Ми все частіше пишемо тексти за допомогою ШІ, і часом це одразу помітно.

Тому я розробив окремий скіл для гуманізації текстів. Він зберігає факти й основний сенс.

Для важливих матеріалів скіл створює кілька варіантів і обирає найсильніший.

В основу я взяв напрацювання з відкритих проєктів і адаптував їх під наш підхід.
"""

AUTHOR_LED_UKRAINIAN = """
У нас накопичилася проста проблема. Текстів із ШІ стало більше, і багато з них начебто нормальні. Але по них одразу видно, як вони написані: однаковий вступ, акуратні абзаци, висновок ні про що.

Я зібрав окремий скіл, бо не хотів щоразу переписувати все руками. Спочатку він фіксує факти й цифри, які не можна втратити. Решту збирає заново під конкретний стиль.

Кілька відкритих проєктів теж стали в пригоді. Частину правил узяли звідти, частину додали вже під себе.
"""


def categories(text: str) -> set[str]:
    return {item["category"] for item in audit(text)["findings"]}


def test_structural_progression() -> None:
    assert "staged_paragraph_progression" in categories(TEMPLATED_UKRAINIAN)
    assert "staged_paragraph_progression" not in categories(AUTHOR_LED_UKRAINIAN)


def test_detector_weight() -> None:
    payload = {
        "original": "The team tested 3 drafts.",
        "candidates": [
            {
                "id": "lower-detector",
                "text": "The team tested 3 drafts.",
                "semantic_score": 1,
                "author_grounding_score": 0.9,
                "voice_score": 0.9,
                "quality_score": 0.9,
                "detector_score": 0.1,
            },
            {
                "id": "higher-detector",
                "text": "The team tested 3 drafts.",
                "semantic_score": 1,
                "author_grounding_score": 0.9,
                "voice_score": 0.9,
                "quality_score": 0.9,
                "detector_score": 0.9,
            },
        ],
        "config": {
            "detector_direction": "lower_is_better",
            "detector_weight": 0.08,
            "require_semantic": True,
            "min_author_grounding": 0.8,
        },
    }
    result = rank_payload(payload)
    assert result["winner"] == "lower-detector"
    assert result["ranking"][0]["derived_scores"]["detector_weight"] == 0.08


def test_adaptive_mining_and_catalog() -> None:
    records = []
    for index in range(10):
        records.append(
            {
                "text": (
                    "Ключовим аспектом цього підходу є послідовна перевірка. "
                    f"PrivateMarker{index} залишається лише в сирому документі."
                ),
                "label": "ai",
                "language": "uk",
                "channel": "social",
                "source": "model-a" if index % 2 == 0 else "model-b",
                "topic": "writing-tools",
            }
        )
        records.append(
            {
                "text": (
                    "Ми перевірили цей варіант на практиці й залишили тільки "
                    f"те, що спрацювало для команди {index}."
                ),
                "label": "human",
                "language": "uk",
                "channel": "social",
                "source": "human-control",
                "topic": "writing-tools",
            }
        )
    mined = mine_records(records, language="uk", channel="social")
    assert mined["warnings"] == []
    assert any(
        item["value"].startswith("ключовим аспектом")
        for item in mined["candidates"]
    )
    assert all(
        item["scope"] == "universal_candidate"
        for item in mined["candidates"]
    )
    serialized = json.dumps(mined, ensure_ascii=False)
    assert "PrivateMarker" not in serialized
    assert "privatemarker" not in serialized
    assert '"text"' not in serialized

    validation_records = []
    for index in range(10):
        validation_records.append(
            {
                "text": (
                    "Ключовим аспектом цього підходу є повторна перевірка. "
                    f"Окремий приклад {index} не зберігається у звіті."
                ),
                "label": "ai",
                "language": "uk",
                "channel": "social",
                "source": "model-c" if index % 2 == 0 else "model-d",
                "topic": "writing-tools",
            }
        )
        validation_records.append(
            {
                "text": (
                    "Ще раз перевірили текст і прибрали пояснення, "
                    f"яке повторювало попередню думку {index}."
                ),
                "label": "human",
                "language": "uk",
                "channel": "social",
                "source": "held-out-human",
                "topic": "writing-tools",
            }
        )
    validated = validate_candidates(
        mined, validation_records, language="uk", channel="social"
    )
    assert validated["validation"]["promotion_ready_candidates"] >= 1
    assert any(
        item["status"] == "validated"
        and item["validation"]["promotion_ready"]
        for item in validated["candidates"]
    )

    checked = audit(
        "Ключовим аспектом цього підходу є перевірка.",
        adaptive_patterns=[
            {
                "id": "test-pattern",
                "status": "active",
                "scope": "universal",
                "kind": "sentence_opening",
                "language": "uk",
                "value": "ключовим аспектом",
            }
        ],
    )
    assert any(
        item["category"] == "adaptive_sentence_opening"
        for item in checked["findings"]
    )

    unchecked = audit(
        "Ключовим аспектом цього підходу є перевірка.",
        adaptive_patterns=[
            {
                "id": "disabled-pattern",
                "status": "disabled",
                "scope": "universal",
                "kind": "sentence_opening",
                "language": "uk",
                "value": "ключовим аспектом",
            }
        ],
    )
    assert not any(
        item["category"] == "adaptive_sentence_opening"
        for item in unchecked["findings"]
    )

    personal_scope = audit(
        "Ключовим аспектом цього підходу є перевірка.",
        adaptive_patterns=[
            {
                "id": "personal-pattern",
                "status": "active",
                "scope": "personal",
                "kind": "sentence_opening",
                "language": "uk",
                "value": "ключовим аспектом",
            }
        ],
    )
    assert not any(
        item["category"] == "adaptive_sentence_opening"
        for item in personal_scope["findings"]
    )


def test_portability_guard() -> None:
    skill_dir = Path(__file__).resolve().parent.parent
    blocked = [
        "".join(("Bog", "dan")).casefold(),
        "".join(("Boh", "dan")).casefold(),
        "".join(("Space", "berry")).casefold(),
    ]
    paths = [
        skill_dir / "SKILL.md",
        skill_dir / "agents" / "openai.yaml",
        *sorted((skill_dir / "references").glob("*.md")),
        skill_dir / "references" / "adaptive-patterns.json",
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8").casefold() for path in paths
    )
    assert not any(value in combined for value in blocked)
    assert "english, ukrainian, and russian" in combined
    assert "#### silent personalization" in combined
    assert "do not ask the user to prepare examples" in combined
    assert "skills run when invoked" in combined
    assert "do not create a scheduler" in combined


def test_reader_first_copywriting_reference() -> None:
    skill_dir = Path(__file__).resolve().parent.parent
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8").casefold()
    copy_text = (
        skill_dir / "references" / "reader-first-copywriting.md"
    ).read_text(encoding="utf-8").casefold()
    manifest = (
        skill_dir / "references" / "source-manifest.md"
    ).read_text(encoding="utf-8").casefold()

    assert "reader-first-copywriting.md" in skill_text
    assert "exact moment" in copy_text
    assert "simplest" in copy_text and "kitchen table" in copy_text
    assert "headline" in copy_text
    assert "microcopy" in copy_text
    assert "subject line" in copy_text
    assert "linkedin" in copy_text
    assert "08b53b1ad39887cd94cbaab61cac3b6aae2d8518" in manifest
    assert "mikiarlo3/ai-copywriter" in manifest


def test_deft_rewrite_payload() -> None:
    payload = build_payload(
        "The source text.",
        rewrite_instructions="Keep every fact and make the prose less formal.",
        style="Direct, plain, restrained.",
    )
    assert payload == {
        "generationMode": "rewrite",
        "prompt": "The source text.",
        "rewriteInstructions": (
            "Keep every fact and make the prose less formal."
        ),
        "thinkingLevel": "human",
        "style": "Direct, plain, restrained.",
        "styleKind": "description",
    }


def test_deft_external_processing_policy() -> None:
    skill_dir = Path(__file__).resolve().parent.parent
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8").casefold()
    deft_text = (
        skill_dir / "references" / "deft-integration.md"
    ).read_text(encoding="utf-8").casefold()

    assert "deft-integration.md" in skill_text
    assert "free web mode" in deft_text
    assert "explicit" in deft_text and "external" in deft_text
    assert "do not bypass" in deft_text
    assert "confidential" in deft_text
    assert "confidentiality controls override" in deft_text
    assert "meaning ledger" in deft_text


if __name__ == "__main__":
    test_structural_progression()
    test_detector_weight()
    test_adaptive_mining_and_catalog()
    test_portability_guard()
    test_reader_first_copywriting_reference()
    test_deft_rewrite_payload()
    test_deft_external_processing_policy()
    print("ok")
