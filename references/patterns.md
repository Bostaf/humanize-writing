# Machine-like writing pattern reference

Use this reference to diagnose writing, not as a mechanical banned-word list. A pattern matters when it appears repeatedly, conflicts with the author's samples, or does no communicative work.

## Contents

- Discourse and reasoning
- Structure and sentences
- Lexical and formatting signals
- Assistant and forensic artifacts
- False positives and false fixes

## Discourse patterns

### Generic orientation

- Opens with broad claims about a rapidly changing world, modern landscape, digital age, or growing importance.
- Delays the actual point behind background the intended reader already knows.
- Uses “In this article, we will explore…” instead of beginning with substance.

### Exhaustive symmetry

- Gives every section the same length and internal structure.
- Covers exactly three advantages, challenges, or considerations without a content reason.
- Gives equal weight to points with clearly unequal importance.

### Staged explanatory progression

- Moves through a frictionless problem → solution → features → conclusion sequence even when the source did not.
- Starts later paragraphs with labels such as “Therefore,” “For important cases,” “As a result,” or “The goal is.”
- Uses Ukrainian patterns such as «Тому я…», «Для важливих матеріалів…», «У результаті…», «В основу я взяв…» as a chain that announces each paragraph's function.
- Makes every paragraph feel independently complete instead of carrying thought or tension forward.

### Repeated conclusion

- Restates the introduction with synonyms.
- Ends every section with a mini-summary.
- Adds a final paragraph about “the future” without a concrete forecast or action.

### Interchangeable paragraphs

- Body paragraphs function as isolated mini-essays and do not build on one another.
- Reordering paragraphs leaves the argument unchanged.
- Each paragraph starts with a fresh thesis rather than advancing the previous one.

### Low information density

- Several sentences restate the same claim in different words.
- “In other words,” “put simply,” and “essentially” introduce no new information.
- Paragraphs are longer than their factual content requires.

### Unearned significance

- Describes ordinary changes as pivotal, transformative, groundbreaking, or a testament to something.
- Claims that an example reflects a broader trend without evidence.
- Adds social or historical importance that is absent from the source.

## Reasoning patterns

### Vague attribution

- “Experts believe,” “research suggests,” “many people,” or “industry leaders” without a source or identifiable group.
- Consensus language used to avoid stating the author's own judgment.

### Automatic balance

- Forces “while X, it is important to remember Y” into a passage that does not need a counterpoint.
- Presents both sides without explaining the author's conclusion.
- Uses hedging to make every claim nearly unfalsifiable.

### Generic causality

- Connects events with “underscores,” “highlights,” or “demonstrates” when the relationship is only asserted.
- Turns correlation or sequence into a causal story.

### Symbolic gloss

- Explains what an ordinary fact “represents,” “embodies,” or “speaks to” without evidence.
- Tells the reader what a concrete detail means when the detail already makes the point.

### False agency

- Gives human intention to an abstraction: “the data tells us,” “the market rewards,” or “the decision wants.”
- Hides the responsible actor behind a system, process, trend, or outcome.

### Unsupported completeness

- Claims a list is comprehensive, robust, holistic, seamless, or end-to-end without defining the boundary.

## Structural patterns

### Template headings

- “Understanding X,” “The importance of X,” “Key benefits,” “Challenges and considerations,” and “The future of X” used as a default outline.
- Headings that merely repeat the topic rather than state useful distinctions.

### Fragmented headers

- A heading is followed by a one-line paragraph that restates it.
- The first substantive information arrives only in the following paragraph.

### Parallel paragraph openings

- Several paragraphs begin with “Additionally,” “Furthermore,” “Moreover,” or the topic name.
- Consecutive sentences repeat the same grammatical frame.

### Mechanical rule of three

- Three adjectives, three clauses, or three benefits recur throughout the text.
- Lists are created for rhythm rather than meaning.

### Excessive signposting

- “It is worth noting,” “It is important to understand,” “This means that,” or “In other words” precedes information that is already clear.

### Diff-anchored writing

- Documentation describes what was changed instead of the current behavior.
- “Now uses,” “was added,” and “replaces the old approach” appear outside changelogs, release notes, or migration guides.

## Sentence patterns

### Mirrored contrast

- “It is not just X; it is Y.”
- “Not only X, but also Y.”
- “Rather than merely X, it fundamentally Y.”

Use occasionally when the contrast is real. Repetition makes the prose feel generated.

### Participial afterthoughts

- Repeated sentences ending in “..., enabling…,” “..., ensuring…,” or “..., highlighting…”.
- The final phrase adds a vague benefit rather than a verifiable consequence.

### Abstract noun stacks

- “The implementation of the optimization of the process…”
- Several nominalizations replace a simpler actor and verb.

### Over-completion

- Every sentence includes context, claim, implication, and benefit.
- No sentence is allowed to remain simple when a simple sentence would be stronger.
- Every paragraph begins with a thesis and ends with a resolved takeaway.
- A short social post reads like a compressed presentation rather than a person's selected observation.

### Manufactured punchlines

- Several short declarations are stacked to create drama.
- Ordinary conclusions are framed as quotable reveals.
- “The catch?”, “The kicker?”, or “Here’s the thing” delays a routine point.

### Aphorism formulas

- Uses templates such as “X is the currency of Y,” “X is where Y meets Z,” or “X is not a tool but a mirror.”
- Replaces a testable claim with reusable profundity.

### Narrator at a distance

- Uses “people tend to,” “one might say,” or “there is a sense that” when a specific actor or the reader could be named.
- Describes an experience from nowhere rather than choosing an informed point of view.

## Lexical patterns

Watch for clusters, not isolated words:

- landscape, realm, journey, tapestry, ecosystem;
- delve, foster, leverage, navigate, unlock, harness;
- crucial, pivotal, robust, seamless, comprehensive;
- innovative, cutting-edge, transformative, game-changing;
- underscore, showcase, testament, ever-evolving;
- moreover, furthermore, additionally, ultimately;
- tailored solutions, valuable insights, meaningful impact;
- “plays a vital role,” “cannot be overstated,” “stands as.”

Use confidence tiers:

- **Tier 1, strong cluster signal**: delve, tapestry used figuratively, testament used figuratively, underscore as a verb, leverage as a verb, multifaceted, realm, interplay, “it is worth noting,” “in today’s … landscape.”
- **Tier 2, density signal**: crucial, pivotal, vibrant, robust, seamless, foster, enhance, showcase, notably, moreover, furthermore, utilize. Treat two or more in a paragraph as meaningful.
- **Tier 3, context only**: key, important, significant, various, effective, valuable, powerful, essential. Never flag one of these alone.

In Ukrainian and Russian, inspect literal translations of the same register:

- «у сучасному світі», «в епоху стрімких змін»;
- «важко переоцінити», «відіграє ключову роль»;
- «комплексний підхід», «безшовний досвід»;
- «підкреслює важливість», «відкриває нові можливості»;
- «динамічний ландшафт», «трансформаційні зміни».

## Formatting patterns

- Heavy use of em dashes where commas or full stops are more natural.
- Bold labels on every bullet.
- A heading for one short paragraph.
- Identical bullet length and syntax.
- Colon-heavy prose that continually announces lists.
- Decorative quotation marks around ordinary terms.

## Assistant and forensic artifacts

- “Of course,” “great question,” “you’re absolutely right,” “I hope this helps,” or offers to continue appear inside publishable prose.
- The text explains what it will cover before covering it.
- Reasoning scaffolding leaks into the result: “let me think,” “breaking this down,” or planning steps intended to remain internal.
- Placeholder tokens, internal citation markers, or tool attribution tags remain in the draft.
- URLs contain unnecessary AI-tool referral parameters.
- Style or error patterns change abruptly between sections.
- Sources are listed as proof instead of explaining what a specific source reported.
- Hidden Unicode, zero-width characters, homoglyph substitutions, or soft hyphens appear.

## Additional high-signal clusters

### Instruction and process leakage

- Mentions the prompt, source instructions, word count target, or editing process inside publishable text.
- Announces “the revised version,” “a more human version,” or a self-assessment that belongs outside the copy.
- Preserves placeholders, synthetic citations, internal labels, or scoring commentary.

### Hedged enumeration

- Every list item begins with “may,” “can,” “could,” or an equivalent hedge.
- A list presents possibilities without ranking them or committing to a recommendation.
- The same caution is repeated at sentence, paragraph, and conclusion level.

### Citation theatre

- Adds sources as decorative authority without tying them to a claim.
- Uses “according to” repeatedly while omitting what the source actually found.
- Places citations after a paragraph containing several claims without showing which claim they support.

### Generic audience simulation

- Uses rhetorical questions whose answer is obvious and that do not reflect a real reader concern.
- Repeats “whether you are X or Y” formulas to simulate broad relevance.
- Uses inclusive “we” without a clear shared group, experience, or decision.

### Simulated author texture

- Adds slang, fragments, confessions, anecdotes, or roughness that are absent from the author's material.
- Applies a named persona as if it were evidence of a specific person's voice.
- Makes a text less formal by adding conversational filler while leaving its templated reasoning untouched.
- Claims to match the author when no authentic sample, note, transcript, or human-authored passage supports the match.

### Uniform resolution

- Every section closes with a takeaway or polished mini-conclusion.
- Uncertainty is converted into generic optimism.
- Tradeoffs disappear in the final paragraph even though they mattered in the body.

Protect legitimate quoted examples, code, citations, proper names, legal language, and UI labels. A quoted AI phrase is not evidence that the surrounding author writes that way.

## False positives

Do not treat any single feature as proof:

- correct grammar or professional editing;
- formal or academic vocabulary;
- one em dash or semicolon;
- one short emphatic sentence;
- one transition word;
- curly typography imposed by Word, macOS, or a CMS;
- clean formatting produced by a template;
- unsourced claims in informal writing;
- dry or bland prose without the clustered patterns above.

Preserve specific, unusual details; mixed feelings; defensible editorial choices; genuine asides; era-bound references; and readable personal quirks.

When detector feedback is involved, distinguish writing quality from provenance. A detector may correctly identify polished or humanized AI prose even when no surface pattern in this reference is present.

## False fixes

Do not:

- inject random spelling or grammar errors;
- replace ordinary words with unusual synonyms;
- alternate sentence length mechanically;
- translate through several languages;
- add irrelevant personal anecdotes;
- imitate dialect, ESL patterns, or informality without evidence;
- insert hidden characters or homoglyphs;
- remove accurate terminology merely because it appears formal.

These tactics often reduce quality, change meaning, or create a new detectable pattern.
