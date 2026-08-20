# Optional Deft integration

Use Deft only when the user explicitly asks for a Deft pass on the current text. Deft is an external writing service, not a required part of Humanize Writing. The local workflow must remain fully usable without it.

The service information below was verified on 2026-08-20. Pricing, quotas, privacy terms, endpoints, and product behavior can change, so verify current official pages before relying on them.

Official pages:

- API: https://deftwriting.com/developers
- Pricing: https://deftwriting.com/pricing
- Rewriter: https://deftwriting.com/rewriter-agent
- Privacy: https://deftwriting.com/privacy
- Terms: https://deftwriting.com/terms

## External-processing gate

An explicit request such as “run this through Deft” authorizes a Deft attempt for that text, subject to these limits. A vague request to “humanize” does not.

Before external processing:

1. Build the meaning ledger and identify protected spans locally.
2. Determine whether the text contains confidential client information, credentials, payment data, government identifiers, health information, private contact details, unpublished strategy, or other sensitive material.
3. Do not send secrets or highly sensitive content. For confidential business material, use a redacted excerpt or ask for explicit confirmation that the user is authorized to submit it to Deft.
4. Tell the user when material will leave the current environment if that is not already obvious from their direct Deft request.
5. Never expose, print, store, or place an API key in the prompt or output.

Deft's published privacy policy says prompts, drafts, outputs, and run metadata may be used to troubleshoot and improve its service unless a separate written agreement says otherwise. Treat this as material when client confidentiality or company policy matters.

## Free web mode

The free website plan currently offers two generations per day. Website generations and API credits are separate. Free website quota cannot be spent through the API.

Use free web mode only through an official user-authorized Deft page and account/session:

1. Finish the local rewrite first.
2. Prefer the official Rewriter or website rewrite mode. Deft recommends complete documents over isolated fragments, but confidentiality controls override that quality preference. Never submit a complete confidential proposal unless the user explicitly confirms authorization after the external-processing and privacy warning; otherwise submit only the redacted minimum necessary excerpt.
3. Ask it to preserve every claim, number, quotation, URL, and qualification; match the intended voice; and avoid inventing details.
4. Retrieve the result through the normal website interface.
5. Compare it locally against the meaning ledger and protected spans. Reject or repair semantic drift before delivery.

Record the authorization decision and redaction scope in the internal handoff or audit record without reproducing confidential content.

When the runtime has an authorized browser capability, it may perform these steps after the user's explicit Deft request. Otherwise, return a compact ready-to-paste Deft handoff containing the text and rewrite instructions. Do not pretend that a manual handoff was submitted.

Do not bypass daily limits, create extra accounts, automate CAPTCHAs, scrape private endpoints, replay session tokens, or disguise website automation as an API call. If the free quota is exhausted, use the local result or ask whether the user wants to use paid API credits.

## API mode

The official server-to-server endpoint is `POST https://deftwriting.com/v1/generate`. API keys belong in the `DEFT_API_KEY` environment variable and must remain server-side.

For a final rewrite use:

- `generationMode: rewrite`;
- the source text in `prompt`;
- bounded transformation requirements in `rewriteInstructions`;
- `thinkingLevel: human` for the strongest writing mode when cost and latency are acceptable;
- an optional compact style description or authentic reference sample.

The bundled `scripts/deft_rewrite.py` builds and sends this request. It requires `--confirm-external-processing` for a live call and supports `--dry-run` for payload inspection. A dry run does not require an API key and sends nothing.

Example:

```bash
python3 scripts/deft_rewrite.py draft.txt \
  --instructions "Preserve every fact and make the prose direct and natural." \
  --confirm-external-processing
```

Successful API requests are billable and the free website allowance does not apply. Never enable auto-recharge, buy credits, or retry a billable request without the user's authorization. Do not automatically retry ambiguous timeouts because the original request may already have completed and incurred cost.

## Local verification after Deft

Treat Deft's output as a candidate, not as the unquestioned final text:

- compare claims, numbers, names, URLs, quotations, and qualifications with the meaning ledger;
- check protected spans exactly;
- check that human-origin passages were not needlessly flattened;
- run the naturalness and copy-specific audits relevant to the channel;
- repair only the affected passages;
- disclose that Deft was used when the user asks about provenance or when a client workflow requires disclosure.

Never claim that Deft makes text human-authored, undetectable, or guaranteed to pass an AI detector.
