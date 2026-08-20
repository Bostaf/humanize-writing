# Source manifest

This manifest records the repository snapshots reviewed for this skill. The original nine sources were reviewed on 2026-07-30; `mikiarlo3/ai-copywriter` was added after a full repository review on 2026-08-20. Repositories were cloned in full, not assessed only from README summaries. Runtime files contain a curated synthesis; model weights, datasets, benchmark outputs, and unrelated project scaffolding are not bundled.

## Audited snapshots

| Repository | Reviewed snapshot | License found | Files and mechanisms reviewed | Integration decision |
|---|---|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | `523374dee72d67c7b2b5f858ea0094ffda49c3ac` | MIT | `SKILL.md`, package validator | Meaning-first reconstruction, clustered pattern audit, fabrication check, voice precedence |
| [harshaneel/humanize](https://github.com/harshaneel/humanize) | `4ec797314537ec9c2105f276d4561d240a0390ba` | MIT | `humanize/SKILL.md`, `ai-check/SKILL.md`, research notes, benchmark scenarios and scripts | Writer-profile distillation, multi-level signal taxonomy, best-of-N and pre-output gate |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | `9a7f35b7b9ad8c3abd71f10757ec9f91fb8ae165` | MIT | Humanizer skill, 53-pattern catalog, templates, tokenizer, scanner, metrics, tests and examples | Protected masking, detect/rewrite/edit modes, newer forensic patterns, MATTR and burstiness metrics |
| [lguz/humanize-writing-skill](https://github.com/lguz/humanize-writing-skill) | `4b7c37fa5148fd499e18498fcc91bb10ed801733` | MIT | Skill, AI-pattern dictionary, voice profiles | Three editing passes, named fallback voices, secondary-convergence check |
| [mikiarlo3/ai-copywriter](https://github.com/mikiarlo3/ai-copywriter) | `08b53b1ad39887cd94cbaab61cac3b6aae2d8518` | MIT | `SKILL.md`, reader-first copywriting mode, format rules, LinkedIn and strategic-blog references, package guidance | Directly adapted reader-state, kitchen-table explanation, copy intake, format-specific drafting, variant, proof, and audit logic; overlapping humanizer patterns deduplicated |
| [YixuanEvenXu/humanization-by-iterative-paraphrasing](https://github.com/YixuanEvenXu/humanization-by-iterative-paraphrasing) | `44062ee8531141e35225335ff98439b9ccd54da5` | MIT | Prompts, iterative inference, trajectory persistence, semantic and detector evaluation, configs | Candidate trajectories, independent 0–10 semantic judge, request traceability and retry design |
| [githigher/MASH](https://github.com/githigher/MASH) | `29428a4cb732d1a7514e37dac8646b5fbf945b5f` | No license file found | README, training stages, hard-negative and sentence-polish pipeline | Architectural ideas only; no source or wording copied |
| [suraj-ranganath/StealthRL](https://github.com/suraj-ranganath/StealthRL) | `6a981cd3a92a57e7558699b5b5694cb4eeba5e04` | MIT | Composite, semantic and quality rewards; evaluation metrics; sanitization; paraphrase baseline | Hard semantic/quality gates, transparent multi-objective ranking, bootstrap-ready evaluation concepts |
| [chengez/Adversarial-Paraphrasing](https://github.com/chengez/Adversarial-Paraphrasing) | `d8515ab705e10b08a1a04214767114522c454bd7` | Apache-2.0 | Detector-guided generation, semantic-equivalence and pairwise quality judges | Independent semantic rubric and pairwise comparison concept; no token-level detector attack code bundled |
| [martiansideofthemoon/ai-detection-paraphrases](https://github.com/martiansideofthemoon/ai-detection-paraphrases) | `95f3e2cb5e239929a1fc4bed26bf93f2c368da31` | Apache-2.0 | DIPPER README, inference controls, samples | Separate lexical-diversity and order-diversity controls; no 11B model or inference code bundled |

## What is incorporated

- Operational instructions distilled into `SKILL.md`.
- Pattern and false-positive guidance in `references/patterns.md`.
- Portable two-layer voice modeling in `references/voice-profile.md`.
- Source-origin handling and human-led editing in `references/author-grounded-workflow.md`.
- Review-gated corpus learning in `references/adaptive-learning.md`.
- Approved cumulative rules in `references/adaptive-patterns.json`.
- Repository-by-repository method decisions in `references/upstream-methods.md`.
- Reader-first marketing and product copy instructions in `references/reader-first-copywriting.md`.
- The high-scrutiny pipeline in `references/research-pipeline.md`.
- Optional external Deft handoff and API behavior in `references/deft-integration.md` and `scripts/deft_rewrite.py`.
- Deterministic multilingual metrics in `scripts/style_audit.py`.
- Privacy-aware contrast mining in `scripts/pattern_miner.py`.
- Fidelity-first candidate gates and ranking in `scripts/candidate_rank.py`.

## Deliberate exclusions

- No pretrained weights, training datasets, detector credentials, or copied benchmark results.
- No promise that a detector will classify a result as human-authored.
- No rewriting tactic is represented as changing AI-authored provenance.
- No fabricated details, random errors, forced burstiness, homoglyph substitutions, or hidden Unicode.
- No MASH source code because the reviewed snapshot did not include a license.
- No script maps Cyrillic letters to Latin lookalikes. Such normalization corrupts legitimate Ukrainian, Russian, and other Cyrillic text.
- No automation bypasses Deft free-tier limits, CAPTCHAs, session controls, or paid API billing.

## Provenance policy

Concepts are rewritten and combined around this skill's fidelity-first architecture. Where a repository supplied directly adapted implementation logic, the repository and license are identified above and in code comments. Apache-2.0 repositories inform interface and evaluation concepts only; their source code is not copied into this package.
