#!/usr/bin/env python3
"""Convert an SRT transcript into timestamped Markdown with optional replacements."""

import argparse
import json
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--title", default="Timestamped transcript")
    parser.add_argument("--note", default="Machine transcript; verify names and terminology.")
    parser.add_argument("--replacements", type=Path, help="JSON object mapping incorrect text to corrected text")
    args = parser.parse_args()

    replacements = {}
    if args.replacements:
        replacements = json.loads(args.replacements.read_text(encoding="utf-8"))

    rows = []
    text = args.source.read_text(encoding="utf-8-sig")
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        if len(lines) < 3 or " --> " not in lines[1]:
            continue
        start, end = [part.replace(",", ".") for part in lines[1].split(" --> ", 1)]
        spoken = " ".join(line.strip() for line in lines[2:] if line.strip())
        for old, new in replacements.items():
            spoken = spoken.replace(old, new)
        rows.append(f"- **[{start}–{end}]** {spoken}")

    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(
        f"# {args.title}\n\n> {args.note}\n\n## Transcript\n\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
