# Author-grounded and detector-aware workflow

Use this reference when a real author's trace matters, the user supplies raw notes or a transcript, or automated detector feedback is part of the evaluation.

## Determine source origin

Classify each source as:

- **Human-authored**: drafted, dictated, or written by the user without generative reconstruction.
- **AI-authored**: generated primarily by a language model, even if later paraphrased.
- **Mixed**: contains identifiable human and AI passages or substantial human revision.
- **Unknown**: origin cannot be established from the request.

Do not convert an origin label through wording alone. Rewriting AI prose may improve quality, but it does not make the source human-authored.

## Preserve the author trace

In human-led work, retain supported signals such as:

- the order in which the author noticed or explained things;
- distinctive but readable phrases;
- uneven emphasis that reflects real priorities;
- concrete examples, constraints, corrections, or uncertainty;
- ordinary repetition where a synonym would sound less natural;
- channel-specific habits in openings, transitions, and endings.

Do not invent anecdotes, mistakes, slang, opinions, or autobiographical details to simulate humanity.

## Choose edit intensity

### Minimal

Use for human-authored drafts and detector-sensitive work.

- Keep paragraph order unless it causes a real comprehension problem.
- Change only wording that is unclear, inaccurate, repetitive beyond the author's habits, or unsuitable for the channel.
- Prefer deletion over replacement when a sentence adds little.
- Preserve a recognizably human base.

### Selective reconstruction

Use for mixed drafts.

- Lock human-origin spans when they are clear and accurate.
- Rebuild only synthetic, generic, or structurally broken passages.
- Recheck transitions at the boundaries between preserved and reconstructed text.

### Full reconstruction

Use for AI-authored drafts or when the user explicitly requests a deep rewrite.

- Build from the meaning ledger rather than the source sentences.
- Ground the result in authentic notes or voice samples when available.
- If no human evidence exists, keep the prose plain and do not claim a personal voice match.

## Audit composition, not only vocabulary

Flag a draft when several of these cluster:

- every paragraph has one neat function;
- paragraphs follow problem → solution → features → conclusion;
- later paragraphs start with explicit stage labels or transitions;
- every sentence is maximally clear, complete, and similarly polished;
- all uncertainty is resolved by the end;
- the text contains no phrase, detail, selection, or emphasis traceable to the author;
- paragraphs can be reordered without changing the argument.

Repair the structure from source evidence. Do not manufacture randomness.

## Use detector feedback responsibly

Record:

- detector and model/version;
- date, language, and word count;
- document label, highlighted segments, and separate confidence value;
- whether the source was human-authored, AI-authored, mixed, or unknown;
- the exact candidate tested.

Interpret a detector as a provenance classifier, not a writing-quality score. A more readable text may still be correctly classified as AI-authored. Short-text warnings, unsupported languages, or low confidence reduce how much weight the result should receive.

When the user explicitly requests detector-aware selection:

1. Compare the raw human control, original AI or mixed draft, and revised candidates when available.
2. Apply fidelity, factuality, and author-grounding gates first.
3. Use detector results to choose among candidates that already pass those gates.
4. Prefer one bounded local repair after feedback.
5. Stop if further edits reduce voice fit, clarity, or factual fidelity.

Never use hidden Unicode, homoglyphs, random errors, mistranslation, fabricated details, or unbounded detector-scored rewriting. Never promise a particular classification.
