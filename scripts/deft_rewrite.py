#!/usr/bin/env python3
"""Build or send an explicit Deft rewrite request.

Live calls require both DEFT_API_KEY and --confirm-external-processing.
The script intentionally does not retry billable requests.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENDPOINT = "https://deftwriting.com/v1/generate"


def build_payload(
    source_text: str,
    *,
    rewrite_instructions: str,
    style: str | None = None,
    thinking_level: str = "human",
) -> dict[str, str]:
    source_text = source_text.strip()
    rewrite_instructions = rewrite_instructions.strip()
    if not source_text:
        raise ValueError("Source text is empty.")
    if not rewrite_instructions:
        raise ValueError("Rewrite instructions are empty.")
    if thinking_level not in {"faster", "smarter", "human"}:
        raise ValueError("thinking_level must be faster, smarter, or human.")

    payload = {
        "generationMode": "rewrite",
        "prompt": source_text,
        "rewriteInstructions": rewrite_instructions,
        "thinkingLevel": thinking_level,
    }
    if style and style.strip():
        payload["style"] = style.strip()
        payload["styleKind"] = "description"
    return payload


def send_payload(payload: dict[str, str], api_key: str) -> dict:
    request = Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Deft HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Deft request failed: {exc.reason}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build or send a Deft rewrite request."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="UTF-8 text file. Reads stdin when omitted.",
    )
    parser.add_argument(
        "--instructions",
        default=(
            "Preserve every claim, number, quotation, URL, qualification, "
            "and factual relationship. Make the prose natural, direct, and "
            "consistent with the supplied author's voice. Do not invent details."
        ),
    )
    parser.add_argument("--style")
    parser.add_argument(
        "--thinking-level",
        choices=("faster", "smarter", "human"),
        default="human",
    )
    parser.add_argument(
        "--confirm-external-processing",
        action="store_true",
        help="Confirm authorization to send this text to Deft.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload without sending it.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the complete JSON response instead of only generated text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_text = (
        Path(args.input).read_text(encoding="utf-8")
        if args.input
        else sys.stdin.read()
    )
    try:
        payload = build_payload(
            source_text,
            rewrite_instructions=args.instructions,
            style=args.style,
            thinking_level=args.thinking_level,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if not args.confirm_external_processing:
        print(
            "Live calls require --confirm-external-processing.",
            file=sys.stderr,
        )
        return 2

    api_key = os.environ.get("DEFT_API_KEY", "").strip()
    if not api_key:
        print("DEFT_API_KEY is not set.", file=sys.stderr)
        return 2

    try:
        result = send_payload(payload, api_key)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    text = result.get("text")
    if not isinstance(text, str):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
