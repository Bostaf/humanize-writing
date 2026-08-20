# Voice profiling

Build a profile from authentic writing samples before matching a person or brand.

## Portable two-layer model

Keep two layers separate:

1. **Universal core**: factual fidelity, source-origin rules, pattern audits, privacy controls, and neutral channel calibration. This layer is safe to share.
2. **Current-user overlay**: observed voice traits, explicit preferences, accepted edits, and negative examples for the author or brand named in the current request.

Do not ship a named user, company, team, or brand profile inside the skill. Do not infer that the person who created or shared the skill is the author of the current text. Never transfer one user's overlay to another user.

Build the overlay from the active user's own messages, supplied samples, notes, transcripts, and direct corrections. Reliable user-specific context exposed by the runtime may also be used when it is clearly attributable to that user. Do not treat shared team documents, generic brand copy, or another person's messages as the user's voice. Update the overlay silently as stronger evidence appears. Use authenticated personal context for cross-session continuity when available. Never place a personal profile or raw samples inside the shared skill package.

## Zero-friction behavior

- Do not ask the user to prepare examples, upload a corpus, approve a profile, or complete onboarding during ordinary text work.
- When no overlay is available, retrieve only relevant writing preferences and prior text feedback through an available personal-context capability.
- Keep the query limited to the current author, language, channel, and writing task. Do not retrieve unrelated personal history.
- Build the profile internally and complete the requested writing task in the same turn.
- Refresh during the next normal invocation when the profile is absent, roughly 30 days stale according to reliable timestamps, or contradicted by a newer correction.
- Do not create a scheduled background task just to refresh the profile. Skills run when invoked.
- Do not announce calibration, refreshes, confidence, or learned traits unless the user asks.
- If no reliable history is available, use the current conversation plus a neutral channel fallback without blocking the task.

## Minimum evidence

When evidence is already available, prefer:

- 3–10 samples;
- at least 500 total words for long-form matching;
- samples from the same channel as the requested output;
- unedited writing when available.

With less evidence, lower confidence internally and use a restrained fallback. State that the match is approximate only when the user asks about accuracy or the distinction materially affects a high-stakes result.

Separate evidence by origin. Authentic human-authored samples, raw notes, and transcripts support a personal voice match. AI drafts approved by the user support preference inference, but do not by themselves establish the user's natural composition.

## Profile dimensions

Record only dimensions supported by examples:

| Dimension | Questions |
|---|---|
| Purpose | Does the author inform, persuade, reassure, challenge, or coordinate? |
| Directness | Do they lead with the conclusion or build toward it? |
| Formality | Conversational, professional, technical, ceremonial? |
| Rhythm | Mostly short, mixed, or developed sentences? |
| Paragraphs | Compact blocks, single-line beats, or extended argument? |
| Vocabulary | Plain, domain-specific, idiomatic, international English? |
| Stance | Decisive, exploratory, skeptical, enthusiastic, restrained? |
| Evidence | Numbers, examples, anecdotes, links, quotations? |
| Transitions | Explicit connectors or mostly implicit flow? |
| Punctuation | Dashes, semicolons, parentheses, fragments, emoji? |
| Formatting | Lists, numbered points, headings, bold labels? |
| Endings | Recommendation, question, summary, invitation, abrupt stop? |

## Separate stable and contextual traits

Stable traits may include directness, tolerance for repetition, preferred vocabulary level, and typical confidence.

Contextual traits may include emoji, sentence length, greetings, technical depth, and calls to action. Match them to the requested channel rather than copying them universally.

## Named fallback profiles

Use these only when authentic samples are unavailable:

| Profile | Characteristics | Best fit |
|---|---|---|
| Clear thinker | Direct, plain vocabulary, mixed sentence length, minimal decoration | Explanations, product writing |
| Casual storyteller | Conversational, first person, contractions, occasional fragments | Social posts, blogs |
| Sharp and opinionated | Strong thesis, explicit tradeoffs, little hedging | Commentary, internal reviews |
| Warm professional | Polite, concrete, short paragraphs, restrained confidence | Client communication |
| Technical | Exact terminology, one claim per sentence, numbers over adjectives | Documentation, engineering |
| Neutral reference | Factual, low-personality, source-conscious, no promotional framing | Research, policy, encyclopedic text |

Infer the profile from the channel and source. Do not force first person, anecdotes, humor, or deliberate irregularity into a register that does not support them.

## Voice replacement rule

Removing a machine-like pattern is insufficient. Replace it with a behavior observed in the samples:

- Replace formal transitions with the author's usual transition style.
- Replace generic emphasis with the author's way of signaling priority.
- Replace assistant-like balance with the author's actual degree of certainty.
- Match the sample's punctuation frequency instead of applying universal punctuation bans.
- Preserve deliberate quirks that remain readable.

Treat disliked samples as negative evidence. Record the contrast between what the user accepts and rejects.

Use evidence strength in this order:

1. direct corrections and explicit constraints in the current request;
2. authentic, channel-matched human writing by the current author;
3. authentic human writing by the same author in another channel;
4. outputs the current author explicitly accepted;
5. neutral channel defaults.

Do not use another person's samples, a shared team corpus, or a profile embedded by the skill creator as personal voice evidence. Do not turn a single correction into a stable rule; prefer repeated corrections or an explicit instruction.

## Author-trace rule

For human-led work, identify at least one supported author trace before editing:

- a distinctive phrase or ordinary repeated word;
- a non-obvious priority or concrete observation;
- the author's order of thought;
- a qualification, aside, correction, or abrupt ending;
- a channel-specific transition or formatting habit.

Preserve it when it remains clear. If the source contains no author trace, do not manufacture one. Use a restrained fallback profile and treat the match as approximate.

## Neutral channel calibration

| Channel | Opening | Body | Ending |
|---|---|---|---|
| Internal decision note | Decision, constraint, or result | Evidence, tradeoff, owner and next action | Concrete ask or next step |
| Client email | Relevant context or answer | Clear operational details; no inflated reassurance | Polite confirmation or question |
| LinkedIn or social | Specific event, observation, or position | One main idea supported by a concrete detail | Grounded implication; no inspirational slogan |
| News brief | Most consequential fact | Group related developments by importance or topic | What changes or what to watch |
| Proposal or case study | Business problem or measurable outcome | Method and evidence in descending importance | Scope, decision, or next action |

Use this table only as a restrained fallback. It is not anyone's personal style.

For English, Ukrainian, and Russian, preserve idiomatic local syntax rather than translating an English profile literally. Keep language-specific overlays separate because the same author may write differently across languages. Do not “normalize” Cyrillic letters into Latin lookalikes. When there is no channel-matched sample, use this table as a fallback and state internally that confidence is limited.

Treat the current user's instructions and authentic samples as higher priority than every fallback.
