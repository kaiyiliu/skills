#!/usr/bin/env python3
"""Combine two timestamp-aligned SRT files into one bilingual SRT."""

import argparse
import re
from pathlib import Path


def read_srt(path: Path) -> list[tuple[str, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) >= 3 and " --> " in lines[1]:
            cues.append((lines[1], "\n".join(lines[2:])))
    return cues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path, help="Language shown on top")
    parser.add_argument("second", type=Path, help="Language shown below")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    first = read_srt(args.first)
    second = read_srt(args.second)
    if len(first) != len(second):
        raise ValueError(f"Cue count differs: first={len(first)}, second={len(second)}")

    blocks = []
    for index, ((time_a, text_a), (time_b, text_b)) in enumerate(zip(first, second), 1):
        if time_a != time_b:
            raise ValueError(f"Timestamp differs at cue {index}: {time_a} != {time_b}")
        blocks.append(f"{index}\n{time_a}\n{text_a}\n{text_b}")

    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
