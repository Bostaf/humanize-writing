---
name: humanize-writing
description: Create, minimally edit, deeply rewrite, or audit prose so writing sounds natural, specific, and consistent with the current author's voice while preserving claims and factual meaning. Use for human-led editing, humanizing AI drafts, removing generic AI-style language, matching the current user's writing style, drafting from notes or transcripts, reviewing detector feedback, auditing machine-like patterns, and revising business, social, editorial, or client-facing writing. Personalize silently from reliable user-specific context when available. Provide dedicated language support for English, Ukrainian, and Russian.
---

# Humanize Writing

Produce credible authorial writing through source-aware editing and structured reconstruction, not synonym substitution. Optimize for voice, specificity, factual fidelity, author grounding, and reader experience. Distinguish human-authored, AI-authored, and mixed source material before editing. Treat automated detector scores as diagnostic signals, never as proof of authorship or the sole quality target.

Keep the shared skill portable and the interaction effortless. Never embed a named user's, brand's, team's, or installer's personal profile in the skill package. Combine a universal core with a current-user voice overlay built silently at runtime from that user's own evidence. Do not turn profile setup into a separate user task. English, Ukrainian, and Russian receive dedicated language rules and evaluation coverage. Handle other languages only through the universal workflow unless the skill is explicitly extended.

## Select a mode

Choose one mode from the request:

1. **Human-led minimal edit**: Preserve a human-authored draft's order, phrasing, emphasis, and readable irregularities while making only necessary local edits.
2. **Draft from source material**: Create prose from notes, a transcript, facts, or an interview.
3. **Deep rewrite**: Reconstruct an existing draft while preserving its claims.
4. **Voice match**: Match authentic samples supplied by the user.
5. **Audit only**: Identify machine-like patterns without rewriting.
6. **Reader-first copywriting**: Write or improve headlines, descriptions, UI microcopy, subject lines, social posts, and strategic marketing prose from verified facts and a specific reader situation.

If the user does not specify a mode, infer it. Prefer human-led minimal edit when the source is genuinely human-authored or detector sensitivity matters. Ask one concise question only when audience, purpose, source origin, or non-negotiable meaning is genuinely ambiguous.

## Load relevant guidance

- Read [references/patterns.md](references/patterns.md) for deep rewrites and audits.
- Read [references/voice-profile.md](references/voice-profile.md) when matching a person or brand.
- Read [references/upstream-methods.md](references/upstream-methods.md) when changing the workflow, running a high-scrutiny rewrite, or explaining which open-source methods are incorporated.
- Read [references/research-pipeline.md](references/research-pipeline.md) for public, brand-sensitive, detector-audited, or otherwise high-scrutiny work.
- Read [references/author-grounded-workflow.md](references/author-grounded-workflow.md) for human-led editing, detector-sensitive work, transcripts, raw notes, or rewrites where preserving a real author's trace matters.
- Read [references/adaptive-learning.md](references/adaptive-learning.md) only for explicit skill-maintenance work that changes the universal pattern catalog.
- Read [references/source-manifest.md](references/source-manifest.md) when provenance, licensing, or the exact upstream integration is relevant.
- Read [references/reader-first-copywriting.md](references/reader-first-copywriting.md) for marketing copy, headlines, meta descriptions, microcopy, subject lines, LinkedIn posts, calls to action, and strategic blog writing.
- Read [references/deft-integration.md](references/deft-integration.md) only when the user explicitly asks to use Deft or asks about a Deft final pass. Deft is optional external processing, never a default stage.
- Run `scripts/style_audit.py` when a text is long enough for quantitative signals or the user asks for an audit. Treat its score as a heuristic, not an AI detector.
- Run `scripts/candidate_rank.py` when high-scrutiny work has multiple candidates or independent semantic, voice, quality, or detector scores.
- Run `scripts/pattern_miner.py` only on explicitly labeled, consented corpora. Treat its output as candidate evidence, not automatically trusted rules.

## Core workflow

### 1. Establish the contract

Identify:

- language, audience, channel, and desired length;
- intended outcome and author position;
- source origin: human-authored, AI-authored, mixed, or unknown;
- facts, names, numbers, quotations, and required terminology;
- supplied style samples and explicit style constraints;
- whether the user wants a clean result, an audit, or both.

Never invent lived experience, quotations, data, citations, or personal opinions. Flag uncertainty instead of smoothing it over.

Do not describe an AI-authored rewrite as human-authored. If the user cares about detector results and only AI-authored material exists, state briefly that editing can improve naturalness but cannot change provenance or guarantee a classification. Prefer authentic raw notes, a transcript, or a human draft as the compositional base.

Identify protected spans before editing: quotations, code blocks, inline code, URLs, citations, product names, legal wording, and user-marked verbatim text. Preserve them exactly unless the user explicitly asks to edit them. Do not count quoted examples or code as evidence about the surrounding author's voice.

### 2. Build a meaning ledger

Before rewriting, privately list:

- claims that must remain;
- supporting evidence and concrete examples;
- qualifications, uncertainty, and disagreement;
- causal relationships;
- calls to action;
- details that may be shortened but not altered.

Use this ledger to verify the final text. Do not expose it unless the user requests an explanation or comparison.

### 3. Build the voice profile

Build a current-user overlay from authentic samples rather than relying on a profile bundled with the skill. Use only evidence attributable to the author or brand named in the current request. Never transfer traits from another user, workspace, brand, or prior install.

#### Silent personalization

Keep personalization invisible unless the user asks about it:

1. When no current-user overlay is available, use a personal-context capability if the runtime provides one. Retrieve only writing-related evidence attributable to the current user: explicit style preferences, prior corrections, accepted or rejected drafts, and authentic examples in the required language or channel.
2. Build a compact in-memory overlay. Do not reproduce the retrieved history, announce calibration, show a profile summary, or ask the user to prepare samples.
3. Refresh the overlay lazily during an ordinary writing request when it is absent, when reliable timestamps indicate that the evidence is roughly 30 days old, when the language or channel changes materially, or when the user supplies a clear new correction.
4. Do not create a scheduler or separate background task solely for refreshing the profile. A skill has no independent background lifecycle; perform the refresh on the next normal invocation.
5. If personal context is unavailable or insufficient, use the current conversation and a restrained channel fallback. Never block the writing task or start an onboarding flow.
6. Keep retrieval narrow. Do not search unrelated personal history, health, finances, private relationships, or other context that cannot affect the requested text.

When authentic samples exist, infer behavior rather than copying phrases:

- sentence and paragraph length distribution;
- preferred level of formality and directness;
- typical openings, transitions, and endings;
- punctuation and formatting habits;
- vocabulary level, contractions, idioms, and code-switching;
- tolerance for fragments, repetition, humor, and uncertainty;
- phrases or tones the author avoids.

Use at least three representative samples when they are already available. Do not ask for them during ordinary text work and do not overfit a single short message. Follow [references/voice-profile.md](references/voice-profile.md).

If no samples exist, infer or select one named profile: clear thinker, casual storyteller, sharp and opinionated, warm professional, technical, or neutral reference. Treat this as channel calibration, not evidence of the person's voice. Do not inject casual personality into legal, academic, technical-reference, or compliance prose.

For detector-sensitive or high-scrutiny work, distinguish author evidence from generic preferences. A request such as “make it natural” is not a voice sample. Prefer phrases, ordering choices, emphasis, and concrete observations found in the user's own material.

Update the runtime overlay silently from the current user's direct corrections, accepted edits, and new authentic samples. Treat corrections as preference evidence and human-authored samples as stronger composition evidence. Rely on authenticated personal context for cross-session continuity when available rather than writing a personal profile into the shared skill. Do not ask the user to manage a catalog or periodically retrain the skill.

### 4. Choose the editing depth

- For human-authored prose, preserve the source's order and locally repair only what blocks the intended result.
- For mixed prose, preserve human-origin passages and reconstruct only clearly synthetic or user-marked sections.
- For AI-authored prose, use the source only for the meaning ledger and rebuild from author evidence or source material.
- For unknown origin, avoid claiming a human-led result and choose the least invasive edit that satisfies the request.

When reconstruction is required:

1. Group related propositions.
2. Choose an order supported by the author's thought process, evidence, or chronology.
3. Preserve at least one authentic author trace where the source supplies one: a distinctive phrase, concrete observation, non-obvious priority, qualification, or transition habit.
4. Reintroduce justified asymmetry. Do not give every point its own equally polished paragraph.
5. Preserve domain terminology where a casual synonym would be less accurate.

Prefer a motivated structure over mechanically varied sentences. Do not “improve” every sentence to the same level of polish.

### 5. Apply multi-level editing

Edit in separate passes:

**Author-grounding pass**

- Verify that personal stance, examples, and distinctive phrases come from the source or authentic samples.
- Preserve readable self-corrections, uneven emphasis, repetition, fragments, or asides when they are genuine.
- Remove simulated personality that was added only to sound human.
- If the text has no author evidence, keep it plain and restrained instead of inventing texture.

**Composition pass**

- Detect overly neat progressions such as problem → solution → benefits → inspirational conclusion.
- Break functional symmetry only when the source supports a different emphasis or order.
- Avoid starting consecutive paragraphs with explanatory labels such as “Therefore,” “For important cases,” “As a result,” or their Ukrainian and Russian equivalents.
- Allow a paragraph to carry more weight than the others when the underlying idea matters more.

**Discourse pass**

- Remove generic scene-setting and summary repetition.
- Make the opening perform useful work immediately.
- Keep only transitions that clarify a real relationship.
- Allow uneven emphasis when some points matter more than others.

**Paragraph pass**

- Vary paragraph size according to purpose.
- Replace exhaustive, symmetrical coverage with deliberate selection.
- Add concrete evidence where the source supports it.
- Remove paragraphs that merely restate a heading.

**Sentence pass**

- Mix short and developed sentences without manufacturing randomness.
- Prefer direct verbs and precise nouns.
- Remove stacked qualifiers, excessive hedging, and polished filler.
- Keep an occasional fragment or informal construction only when it fits the voice and channel.

**Lexical pass**

- Replace generic intensifiers and AI-associated stock phrases.
- Avoid thesaurus substitutions that change register or meaning.
- Preserve recurring words when repetition is clearer than artificial synonym variety.

**Assistant-voice pass**

- Remove chat framing, acknowledgments, offers to continue, unnecessary definitions, recap paragraphs, and unrequested option lists.
- Replace automatic balance with the actual asymmetry or conclusion.
- Delete reasoning scaffolding that belongs in analysis rather than published prose.
- Normalize register shifts introduced by separate AI-generated sections.

### 6. Run an adversarial editorial audit

Review the candidate from two independent perspectives:

**Forensic editor**

- Locate templated openings, staged paragraph progressions, rule-of-three habits, mirrored contrasts, inflated significance, generic conclusions, vague attribution, empty transitions, false agency, aphorism formulas, theatrical hooks, excessive balance, and uniformly resolved paragraphs.
- Identify any paragraph that could fit hundreds of unrelated topics.
- Run the paragraph-reshuffle test: if two body paragraphs can swap places without damaging the argument, strengthen the dependency, merge them, or remove one.
- Run the information-density test: ask what each sentence adds that the previous sentence did not.
- Run the author-trace test: identify what in the wording or selection of detail could plausibly belong to this author rather than any competent writer. If the answer is “nothing,” return to authentic source material instead of adding fabricated quirks.

**Human reader**

- Ask whether the writer appears to know why they are saying each sentence.
- Check whether the text contains a recognizable position, selection of detail, and audience awareness.
- Mark language that is correct but implausible for the claimed author or channel.

Revise only the flagged passages. Do not repeatedly paraphrase the entire document; whole-text iteration increases semantic drift and homogenization.

### 7. Use a candidate tournament when scrutiny is high

For important public writing, produce three internally held candidates with genuinely different composition strategies:

1. direct conclusion first;
2. concrete example or scene first;
3. author-led source-order or compressed plain-language version.

Do not create three synonym variants of the same structure. Track lexical change and structural/order change separately; treat them as bounded controls, not targets to maximize. Audit each candidate independently for fidelity, factuality, voice similarity, specificity, coherence, protected-span preservation, and clustered patterns.

For sensitive work, use the independent evaluation and trajectory record in [references/research-pipeline.md](references/research-pipeline.md). Apply hard fidelity gates before ranking. A detector result, when supplied, is a minor diagnostic signal and cannot override missing claims, invented details, or voice mismatch. Select the strongest candidate, then perform one local corrective pass. Return only the winner unless the user asks to compare versions.

### 8. Verify quality gates

Do not deliver until all applicable gates pass:

- **Fidelity**: Every material claim matches the meaning ledger.
- **Factuality**: No unsupported fact, quote, number, or personal detail was added.
- **Voice**: The draft follows observed habits rather than a generic persona label.
- **Origin honesty**: The result does not imply human authorship when the prose was generated or substantially reconstructed by AI.
- **Author grounding**: Personal texture is supported by human source material or authentic samples.
- **Specificity**: Important assertions have concrete referents where the source permits.
- **Coherence**: Variation does not damage logic or readability.
- **Naturalness**: The text avoids the patterns in `references/patterns.md`.
- **Protection**: Code, quotations, URLs, citations, and verbatim wording remain intact.
- **Format**: Length, language, channel, and user constraints are satisfied.

If automated detector results are supplied, use highlighted passages as leads for editorial inspection. Never promise a detector outcome. Modern systems differ, change over time, and can label genuine human writing incorrectly.

### 9. Maintain the universal catalog only with controls

Treat universal pattern learning as optional maintainer work, never as part of normal text optimization. When a skill maintainer explicitly asks to update the shared catalog:

1. Confirm or infer only defensible origin labels. Do not use a detector prediction as ground-truth authorship.
2. Keep human and AI controls comparable by language, channel, and approximate length.
3. Run `scripts/pattern_miner.py` to produce aggregate candidates. Do not store raw texts in the skill.
4. Separate universal AI-pattern learning from current-user voice learning. Never promote an author's recurring preference as an AI pattern.
5. Reject candidates supported by too few AI documents, one generator/source only, one author's style, or a material share of human controls.
6. Validate proposed patterns on held-out texts that were not used for mining.
7. Promote only reviewed, cross-author patterns with `scope: universal` to `references/adaptive-patterns.json`, then rerun regression tests and inspect false positives.

Never modify the active catalog during an ordinary rewrite. Universal promotion requires an explicit maintenance request. Runtime adaptation to the current user's direct corrections may happen automatically, but it must not alter the shared catalog. Follow [references/adaptive-learning.md](references/adaptive-learning.md).

## Mode-specific instructions

### Human-led minimal edit

Treat the supplied human draft, notes, or transcript as the primary composition. Preserve its order of thought, ordinary vocabulary, natural repetition, and channel-appropriate rough edges. Make local edits for clarity, accuracy, grammar, or length. Do not rebuild the text into a polished template. When useful, provide a compact change summary or tracked comparison.

### Draft from notes or transcript

Preserve the source's order of thought when it contributes personality, but remove transcription noise. Retain distinctive turns of phrase that are clear. Do not expand sparse notes with generic filler. If crucial substance is missing, ask targeted questions or leave a compact placeholder.

### Deep rewrite

Use the source only to construct the meaning ledger, then draft from that ledger. Compare the result against the original for omissions and semantic drift. Restore any lost qualification or evidence before polishing.

If the source is AI-authored, do not expect repeated paraphrasing to erase its provenance. Improve reader quality and voice fit, but prefer human notes or samples before attempting a detector-sensitive rewrite.

### Voice match

Separate stable author habits from channel-specific conventions. A person's email, LinkedIn post, and formal proposal should not be flattened into one register. Prefer structural and pragmatic similarity over copied catchphrases.

Personalize for the current author only. Do not assume the skill creator's voice, the installer's identity, or a bundled named profile. When evidence is sparse, use a restrained channel fallback and describe the match as approximate if that qualification matters.

### Audit only

Return:

1. a brief overall assessment;
2. the most consequential patterns, with exact excerpts;
3. why each pattern weakens authenticity or quality;
4. quantitative style signals when the audit script is useful;
5. targeted revision guidance.

Do not rewrite unless requested.

### Reader-first copywriting

Start from the reader's exact situation and the simplest accurate explanation, not from product adjectives. Identify the primary promise, available proof, likely objection, and job of the requested format. Use only facts supplied by the user or a named source. Follow [references/reader-first-copywriting.md](references/reader-first-copywriting.md), then run the normal fidelity and naturalness gates.

If the brief lacks a fact needed for a strong claim, write the strongest grounded version and ask only the one question that would materially improve it. Do not turn ordinary copy work into a mandatory intake interview.

### Universal pattern maintenance

Return a compact corpus summary, candidate patterns with aggregate evidence, false-positive risks, and a promotion recommendation. Do not reproduce uploaded documents or save them inside the skill. If the user also authorized updating the skill, promote only candidates that pass the documented validation gates.

## Output rules

- Lead with the revised text when the user asked for a deliverable.
- Keep process commentary brief.
- Do not add an AI-detection score unless the user asked for an audit.
- When detector performance is requested, report only results actually supplied or obtained, including service, model/version, language, length, and confidence when available.
- When the user wants only the rewritten text, return no preamble, self-review, or changelog.
- Do not mention silent personalization, retrieved context, profile refreshes, or internal confidence unless the user asks or a material privacy or reliability limitation must be disclosed.
- Do not intentionally add spelling mistakes, grammar errors, Unicode homoglyphs, hidden characters, fabricated anecdotes, or false citations.
- Do not claim that a result is “undetectable,” “100% human,” or guaranteed to pass a service.
- Respect authorship and disclosure rules for academic, legal, hiring, compliance, or other high-stakes contexts.
- Never send text to Deft or another external writing service unless the user explicitly requests that service for the current text. Follow [references/deft-integration.md](references/deft-integration.md) for consent, confidentiality, free-web, and API behavior.
