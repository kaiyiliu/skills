#!/usr/bin/env python3
"""Merge adjacent short SRT cues without changing their outer timestamps."""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Cue:
    start_text: str
    end_text: str
    start: float
    end: float
    text: str


def seconds(value: str) -> float:
    hours, minutes, rest = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(rest)


def read_srt(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) < 3 or " --> " not in lines[1]:
            continue
        start, end = lines[1].split(" --> ", 1)
        cues.append(Cue(start, end, seconds(start), seconds(end), " ".join(lines[2:])))
    return cues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--max-gap", type=float, default=0.65)
    parser.add_argument("--max-duration", type=float, default=6.5)
    parser.add_argument("--max-chars", type=int, default=46)
    parser.add_argument("--separator", default=" ")
    args = parser.parse_args()

    source = read_srt(args.source)
    merged: list[Cue] = []
    for cue in source:
        if merged:
            previous = merged[-1]
            combined = previous.text.rstrip() + args.separator + cue.text.lstrip()
            if (
                cue.start - previous.end <= args.max_gap
                and cue.end - previous.start <= args.max_duration
                and len(combined.replace(" ", "")) <= args.max_chars
            ):
                previous.end_text = cue.end_text
                previous.end = cue.end
                previous.text = combined
                continue
        merged.append(cue)

    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(
        "\n\n".join(
            f"{index}\n{cue.start_text} --> {cue.end_text}\n{cue.text}"
            for index, cue in enumerate(merged, 1)
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Merged {len(source)} cues into {len(merged)} cues")


if __name__ == "__main__":
    main()
