# Upstream methods incorporated

This skill combines compatible ideas from open writing skills and research repositories audited at the file level. See [source-manifest.md](source-manifest.md) for pinned snapshots, licenses, reviewed files, and exclusions. Use the sources as design inputs, not as evidence that any text is human-authored or guaranteed to pass a detector.

## Open-source skills

### blader/humanizer

Source: https://github.com/blader/humanizer

Adopted and adapted:

- preserve information rather than source shape;
- explicit fabrication check;
- voice samples outrank universal style rules;
- clustered pattern detection;
- draft, forensic audit, corrective pass;
- pattern families based on Wikipedia's Signs of AI writing.

### harshaneel/humanize

Source: https://github.com/harshaneel/humanize

Adopted and adapted:

- idea-level re-derivation instead of light synonym editing;
- removal of RLHF and helpful-assistant framing;
- writer-profile distillation;
- specificity inventory;
- separation of surface, structural, discourse, and voice signals;
- explicit pre-output quality gate.
- best-of-N candidate selection.

Rejected:

- detector-scored optimization loops as a default workflow;
- fabricated “plausible specificity”;
- universal punctuation claims that conflict with a supplied voice sample.

### Aboudjem/humanizer-skill

Source: https://github.com/Aboudjem/humanizer-skill

Adopted and adapted:

- detect, rewrite, and targeted-edit modes;
- named voice profiles;
- masking quoted and code content;
- emerging forensic patterns such as false agency, paragraph interchangeability, diff-anchored writing, reasoning artifacts, and Unicode obfuscation;
- deterministic metrics treated as heuristics rather than proof.
- moving-average type-token ratio and sentence-length burstiness added to the local audit.

Rejected:

- claims that a low internal score means no detector will flag the text;
- forced burstiness and personality injection without register evidence;
- repeated whole-document iteration until an internal score reaches zero.

### lguz/humanize-writing-skill

Source: https://github.com/lguz/humanize-writing-skill

Adopted and adapted:

- separate lexical, structural, and texture passes;
- explicit voice selection;
- secondary-convergence check so one cliché is not replaced by another;
- paragraph endings that do not mechanically recap.

### mikiarlo3/ai-copywriter

Source: https://github.com/mikiarlo3/ai-copywriter

Adopted and adapted directly into `reader-first-copywriting.md`:

- reader state at the exact moment a line is encountered;
- a kitchen-table simplicity test before drafting;
- primary promise, proof, objection, action, category, and story as copy inputs;
- distinct jobs and constraints for headlines, descriptions, microcopy, subject lines, LinkedIn posts, and strategic marketing prose;
- genuinely different variant angles instead of synonym cycling;
- copy-specific audit questions based on reader state, repeatability, standalone clarity, and supplied proof;
- no-fabrication rules for metrics, stories, quotes, product facts, and vulnerability.

Rejected or narrowed:

- mandatory multi-question intake for every request, because this skill prioritizes zero-friction operation and asks only when a missing fact materially changes the result;
- clickbait and virality as general objectives;
- duplicating the upstream 33-pattern list, which derives from `blader/humanizer` and is already covered by this skill's broader multilingual, clustered pattern system;
- universal bans on punctuation or typography that conflict with authentic author evidence.

## Research-inspired architecture

- HIP: store candidate trajectories, separate semantic evaluation from detector evaluation, and use low-distortion iterative transformation. The prompt-only skill does not claim to implement HIP's LoRA paraphraser.
- MASH: treat style transfer as staged alignment with selective sentence repair, not banned-word substitution. The audited snapshot had no license file, so no code or wording is copied.
- StealthRL: use hard semantic and quality thresholds before multi-objective ranking. Reject its Cyrillic-to-Latin homoglyph sanitization for multilingual prose.
- Adversarial Paraphrasing: use an independent semantic-equivalence rubric and pairwise quality comparison. Do not bundle detector-guided token attack code.
- DIPPER: control lexical diversity separately from order diversity. Neither should be maximized blindly.

## Combined operating model

1. Classify source origin and protect human-origin as well as immutable spans.
2. Extract a meaning ledger and authentic author traces.
3. Distill or infer voice without treating a generic persona as authorship evidence.
4. Choose minimal editing, selective reconstruction, or full reconstruction based on source origin.
5. Apply author-grounding, composition, lexical, structural, discourse, and assistant-voice passes.
6. Audit patterns, paragraph progression, and quantitative signals independently.
7. Verify facts, author grounding, and protected spans with hard gates.
8. For high scrutiny, compare structurally different candidates through the pipeline in [research-pipeline.md](research-pipeline.md).

## Licensing notices

Adapted concepts and portions are used under MIT licenses:

- Copyright (c) 2025 Siqi Chen, blader/humanizer.
- Copyright (c) 2026 Harshaneel Gokhale, harshaneel/humanize.
- Copyright (c) 2026 Adam Boudjemaa, Aboudjem/humanizer-skill.
- Copyright (c) 2026 Luis Guzman, lguz/humanize-writing-skill.
- Copyright (c) 2026 Mickey Haslavsky, mikiarlo3/ai-copywriter copywriting additions.
- Copyright (c) 2026 The HIP Authors, humanization-by-iterative-paraphrasing.
- Copyright (c) 2025 StealthRL Authors, StealthRL.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, and to permit persons to whom the software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
