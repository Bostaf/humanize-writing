# Humanize Writing

Humanize Writing is a portable AI skill for making generated or heavily edited prose sound more natural while preserving facts, meaning, and the author's real voice.

It supports English, Ukrainian, and Russian and works with ChatGPT, Claude, Codex, and other tools that can load Markdown-based agent skills.

## What makes it different

- Preserves claims, numbers, quotations, URLs, and protected wording.
- Distinguishes human-authored, AI-authored, mixed, and unknown source material.
- Uses minimal editing for dictated or genuinely human drafts.
- Reconstructs synthetic drafts from a meaning ledger instead of swapping synonyms.
- Adapts silently to the current user's writing preferences and previous corrections.
- Audits structural, lexical, discourse, formatting, and assistant-style AI patterns.
- Includes a reader-first copywriting mode for headlines, microcopy, metadata, emails, LinkedIn, and marketing prose.
- Maintains a review-gated catalog for learning new universal AI-writing patterns without storing raw documents.
- Supports optional Deft web and API passes with confidentiality and fidelity checks.

The skill combines reviewed methods from ten open-source projects and several research approaches. See [`references/source-manifest.md`](references/source-manifest.md) for exact snapshots, licenses, adopted mechanisms, and exclusions.

## Installation

### ChatGPT

Download the repository as a ZIP, attach it to a new chat, and ask ChatGPT to install the skill. After installation, invoke `Humanize Writing` or mention it in a writing request.

### Claude

Upload the repository ZIP through Claude's Skills settings and enable it. Claude may select it automatically, or you can ask it to `Use Humanize Writing`.

### Codex and compatible agent runtimes

Install the `humanize-writing` folder in the runtime's skills directory, then invoke `$humanize-writing` or make a request that matches the skill description.

## Usage

For a dictated or human-written draft:

```text
This is my dictated text. Keep my wording and order of thought, fix mistakes,
remove unnecessary repetition, and improve the rhythm only where needed.
```

For an AI-generated draft:

```text
Make this text more natural without changing any facts, numbers, links,
qualifications, or the main meaning.
```

For copywriting:

```text
Write five distinct homepage headlines and a 155-character meta description.
Use only the supplied product facts and write for a skeptical operations manager.
```

For an optional Deft pass:

```text
Run the final version through Deft, then verify every fact and protected span
against the source before returning it.
```

Deft's free website allowance and paid API credits are separate. The skill never bypasses quotas, submits confidential material by default, or treats an external rewrite as automatically correct.

## Main modes

1. Human-led minimal edit
2. Draft from notes or transcript
3. Deep rewrite
4. Voice match
5. Audit only
6. Reader-first copywriting

## Validation

Run the deterministic regression checks from the repository root:

```bash
python3 scripts/test_humanize.py
```

The included scripts are editorial heuristics and workflow helpers, not proof of authorship and not a guarantee that any detector will classify a text as human-written.

## Repository structure

- `SKILL.md`: skill entry point and core workflow
- `references/`: pattern catalog, voice model, research pipeline, provenance, copywriting, and Deft guidance
- `scripts/`: style audit, candidate ranking, adaptive pattern mining, Deft API adapter, and regression tests
- `agents/openai.yaml`: ChatGPT and Codex interface metadata

## Limitations

Humanize Writing improves editorial quality and voice fit. It does not change the provenance of AI-generated material, fabricate human experience, or guarantee results from AI detectors.
# humanize-writing
Humanize AI-generated writing while preserving facts, meaning, and author voice.
