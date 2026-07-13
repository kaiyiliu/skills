#!/usr/bin/env python3
"""Remap an SRT through kept source spans described by a JSON timeline."""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Cue:
    start: float
    end: float
    text: str


def parse_time(value: str) -> float:
    value = value.replace(",", ".")
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def format_time(value: float) -> str:
    total_ms = max(0, round(value * 1000))
    hours, total_ms = divmod(total_ms, 3_600_000)
    minutes, total_ms = divmod(total_ms, 60_000)
    seconds, milliseconds = divmod(total_ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def read_srt(path: Path) -> list[Cue]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) >= 3 and " --> " in lines[1]:
            start, end = lines[1].split(" --> ", 1)
            cues.append(Cue(parse_time(start), parse_time(end), "\n".join(lines[2:])))
    return cues


def cue_from_json(item: dict) -> Cue:
    return Cue(float(item["start"]), float(item["end"]), str(item["text"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("timeline", type=Path, help="JSON with keep_spans and optional prepend_cues")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    source = read_srt(args.source)
    spec = json.loads(args.timeline.read_text(encoding="utf-8"))
    output = [cue_from_json(item) for item in spec.get("prepend_cues", [])]
    destination = float(spec.get("timeline_offset", 0.0))
    if output:
        destination = max(destination, max(cue.end for cue in output))

    for span in spec["keep_spans"]:
        span_start = float(span["source_start"])
        span_end = float(span["source_end"])
        if span_end <= span_start:
            raise ValueError(f"Invalid keep span: {span}")
        for cue in source:
            overlap_start = max(cue.start, span_start)
            overlap_end = min(cue.end, span_end)
            if overlap_end > overlap_start:
                output.append(
                    Cue(
                        destination + overlap_start - span_start,
                        destination + overlap_end - span_start,
                        cue.text,
                    )
                )
        destination += span_end - span_start

    parts = []
    for index, cue in enumerate(sorted(output, key=lambda item: (item.start, item.end)), 1):
        if cue.end - cue.start >= 0.08:
            parts.append(f"{index}\n{format_time(cue.start)} --> {format_time(cue.end)}\n{cue.text}")
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
