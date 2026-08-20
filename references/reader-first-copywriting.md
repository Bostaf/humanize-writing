# Reader-first copywriting

Use this mode for copy whose job is to earn attention or help a reader act: headlines, short descriptions, meta descriptions, UI microcopy, calls to action, subject lines, LinkedIn posts, and strategic marketing prose.

This reference directly adapts the copywriting mode from `mikiarlo3/ai-copywriter` at snapshot `08b53b1ad39887cd94cbaab61cac3b6aae2d8518`. The upstream skill is Markdown code licensed under MIT. Its copywriting additions are Copyright (c) 2026 Mickey Haslavsky; its original humanizer material is Copyright (c) 2025 Siqi Chen. The full license notice is retained in [upstream-methods.md](upstream-methods.md).

## The two questions behind every line

Answer these privately before drafting:

1. **What is the reader feeling at the exact moment this line reaches them?** A person mid-scroll is bored and nearly gone. Someone reading an error is frustrated and wants the fix. A buyer comparing tabs is skeptical and wants proof. The moment decides the tone, length, and what comes first.
2. **What is the simplest accurate way to explain this?** Use the words you would use across a kitchen table. Prefer common words, one thought at a time, and nothing the reader must decode or reread.

Do not force a long interview. Extract what the request already establishes. Ask one targeted question only when a missing fact, audience, or action would materially change the result. In embedded or no-interaction contexts, write from available evidence and state the important gap compactly.

## Build the message contract

Identify:

- the exact reader and their current situation;
- the mental category they will compare this with;
- the primary promise;
- the strongest supplied proof;
- the objection the copy must resolve;
- the action the reader should take;
- the real story, number, mechanism, or observation that makes the copy specific.

Translate facts into reader vocabulary without inventing benefits. A measured result from one case is evidence, not a universal guarantee. Qualify it when scope is limited.

## Make the source worth writing from

For story-led copy, test the supplied material:

- Is there a number that changes how the reader sees the claim?
- Was there a near-failure, constraint, or tradeoff?
- Did the author believe something that turned out wrong?
- Is there a true detail they would tell another person without being prompted?

If none exists, keep the copy plain. Do not fabricate a dramatic story, customer quote, vulnerability, metric, or personal experience.

## Format rules

### Headlines and titles

- Lead with the sharpest supplied detail: result, number, contradiction, named problem, or mechanism.
- A curiosity gap may withhold the answer, never the subject. The content must close the gap.
- Use the reader's words rather than the industry's abstractions.
- Avoid generic hype such as `ultimate`, `game-changing`, `unlock`, `elevate`, `revolutionize`, `secrets`, and `you won't believe` unless the quoted brand voice genuinely uses it and the claim remains supportable.
- When variants are requested, produce genuinely different angles rather than synonym swaps: outcome, problem, question, contradiction, how-to, mechanism, or named enemy.
- Recommend one option based on the reader's situation, clarity, specificity, and credibility, not because it is merely “punchier.”

### Short and meta descriptions

- Put the benefit or concrete action in the opening words.
- Keep one main idea per description.
- Respect the requested character budget by counting characters. Cut secondary ideas instead of compressing the sentence into unnatural fragments.
- Preserve the subject and important search terms when writing SEO metadata; do not turn it into a list of keywords.

### UI microcopy

- Identify the user's state, what just happened, and the next useful action.
- Buttons name the result: `Send invoice`, not `Submit`.
- Errors say what went wrong and how to fix it, without blame.
- Empty states explain the first useful action rather than apologizing for missing data.
- Destructive confirmations state the consequence and whether it can be undone.
- Match the product's established case and punctuation conventions.

### Subject lines and hooks

- Write to one person in one situation, not to an abstract segment.
- Front-load the concrete payoff because previews are short.
- Do not use fake urgency, fake familiarity, or vague bait.
- The hook must accurately preview the payoff. Withholding context to manufacture dwell time weakens trust.

### LinkedIn posts

- The opening two lines carry a specific event, observation, or position.
- Build the post around one true story or one defensible stance.
- Preserve one portable claim the intended professional audience could repeat accurately.
- Use surprise, stakes, or productive tension without rage bait or fabricated conflict.
- Short paragraphs are a channel convention, not a quota. Every line must add information.
- Never invent a conversation, firing, customer message, number, or “DM I got this morning.”
- End with a grounded implication or a substantive question. Avoid `Thoughts?`, engagement bait, and requests to repost.
- When useful, offer several distinct hooks and build the full post from the strongest one.

### Strategic marketing and blog writing

- Start with the broken assumption or changed condition, not generic background.
- State the contradiction that makes the piece worth reading.
- Organize evidence into a framework only when the evidence supports one.
- Company examples must explain the mechanism, not merely name a result.
- Separate verified facts from interpretation and qualify uncertain causation.
- End with an operating implication, not a generic optimistic conclusion.

## Copy-specific audit

Before delivery, ask:

1. What is the reader feeling when this line reaches them, and does the line meet that state?
2. Can the reader repeat the promise after one read?
3. Is the promise supported by a supplied fact, mechanism, or source?
4. Does each requested format perform its own job rather than reuse one uniform sentence?
5. Would the line still make sense by itself, without the surrounding variants or explanation?

Then run the skill's normal fidelity, author-grounding, protected-span, naturalness, and format gates.

## What not to inherit mechanically

The upstream repository contains a broad humanizer pattern list inherited from `blader/humanizer`. This skill already maintains a larger clustered pattern reference, multilingual rules, false-positive controls, source-origin handling, and adaptive learning. Use the upstream copywriting code directly through this mode, but do not duplicate overlapping pattern wording or replace the current fidelity-first architecture.
