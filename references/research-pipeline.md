# High-scrutiny pipeline

Use this pipeline for public, brand-sensitive, or detector-audited writing. It is an editorial quality system, not a guarantee about authorship classifiers.

## Architecture

### Tier A: contract and invariants

Create the meaning ledger and voice contract before generation. Mask quotations, code, URLs, citations, names, numbers, legal text, and user-marked verbatim spans. A candidate that drops or invents a protected literal fails regardless of every other score.

Record source origin as human-authored, AI-authored, mixed, or unknown. Identify human-origin spans and author evidence separately from facts. Origin does not change because a draft was paraphrased.

### Tier B: structurally distinct candidates

Generate two to four candidates from the ledger, not from successive whole-document paraphrases. Vary the composition strategy:

- conclusion first;
- concrete evidence or example first;
- compressed plain-language version;
- author-led source-order version when the human source's chronology or thought sequence carries meaning.

Track lexical change and order/structure change separately. These are controls, not objectives to maximize. Too little change retains the source template; too much increases semantic drift.

For each candidate, retain:

- source or parent candidate;
- generation strategy;
- prompt or instruction version;
- optional lexical and order-diversity controls;
- semantic, voice, quality, and detector results;
- exact gate failures;
- final editorial decision.

This trajectory record adapts HIP's checkpointed iterative evaluation without requiring its LoRA model.

### Tier C: independent evaluation

Evaluate a candidate independently from the generation pass.

1. **Deterministic fidelity gate**: protected literals, URLs, code, quotations, numbers, suspicious Unicode.
2. **Semantic judge**: score preservation of claims, relationships, qualifications, and intent. Prefer a separate model or human review. Use a 0–1 or 0–10 rubric consistently.
3. **Voice judge**: compare directness, formality, rhythm, evidence use, punctuation, and endings against authentic samples.
4. **Author-grounding judge**: verify that personal texture comes from human material and that human-origin passages were not needlessly reconstructed.
5. **Quality judge**: assess coherence, grammar, information density, unsupported specificity, and channel fit.
6. **Style audit**: inspect clustered patterns, paragraph progression, and metrics; do not turn a heuristic into an authorship verdict.
7. **Optional detector signal**: record the service, model/version, date, language, word count, displayed label, confidence, and score direction. Never let it override fidelity, factuality, or author grounding.

When quality differences are close, compare candidates pairwise rather than relying only on absolute scores.

### Tier D: selection and local repair

Apply hard gates first. Rank only candidates that pass. The default ordering is:

1. fidelity and factuality;
2. author grounding;
3. voice match;
4. editorial quality;
5. pattern audit;
6. optional detector signal.

Use `scripts/candidate_rank.py` for a transparent local implementation. Repair only the rejected passage or sentence. Re-run the relevant gates after repair. Avoid unbounded whole-document loops.

## Candidate-ranker input

```json
{
  "original": "The source text with 27% and https://example.com.",
  "candidates": [
    {
      "id": "direct",
      "text": "A revision preserving 27% and https://example.com.",
      "semantic_score": 0.96,
      "author_grounding_score": 0.92,
      "voice_score": 0.84,
      "quality_score": 0.9,
      "detector_score": 0.42
    }
  ],
  "config": {
    "min_semantic": 0.9,
    "require_semantic": true,
    "min_author_grounding": 0.7,
    "min_voice": 0.7,
    "min_quality": 0.75,
    "detector_direction": "lower_is_better",
    "detector_weight": 0.08,
    "required_literals": ["Example Product"],
    "lexical_change_target": [0.12, 0.6],
    "structural_change_target": [0.18, 0.85]
  }
}
```

The semantic, voice, quality, and detector fields are optional, but important work should supply independent semantic and voice assessments. The ranker defaults to a two-percentage-point detector contribution. When the user explicitly requests detector-aware selection, `detector_weight` may increase the contribution up to ten percentage points after all hard gates pass.

Do not treat an output score such as “100% AI” as calibrated confidence unless the detector documentation says it is. Preserve document coverage, class confidence, and probability-like scores as separate fields.

## Optional model-backed extension

A future plugin or service can add:

- a HIP-style iterative paraphraser;
- a MASH-style style-transfer and selective sentence-refinement stage;
- a StealthRL-style multi-objective trained policy;
- a DIPPER-style backend with separate lexical and order controls;
- detector adapters with versioned responses;
- a model-based semantic and pairwise quality judge.

Keep this backend outside the skill package. The skill should remain usable without GPU weights, paid detector access, or a specific model provider. The backend must return candidates and scores through the same transparent contract and may not bypass the hard fidelity gates.

Deft may be used as one optional external rewrite candidate when the user explicitly requests it. Follow [deft-integration.md](deft-integration.md): external-processing and confidentiality rules apply before submission, while the same fidelity, author-grounding, and protected-span gates apply after retrieval. Website free quota and paid API credits are separate; neither changes the ranking contract.

## Evaluation protocol

Build a held-out set from authentic channel-matched writing and difficult rewrites in English, Ukrainian, and Russian. Include numbers, URLs, quotations, mixed scripts, technical terms, short messages, and long-form prose.

Report:

- protected-span preservation;
- semantic pass rate and human-reviewed drift;
- voice preference against a baseline;
- factual additions and omissions;
- edit distance, lexical change, and structural change;
- readability and clustered-pattern findings;
- detector results by service and version, with false positives on authentic human text;
- source origin and the amount of human-authored material preserved;
- confidence intervals for aggregate results.

Do not tune and report on the same examples. Detector-only gains do not count when semantic or human preference declines.
