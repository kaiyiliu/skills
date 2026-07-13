#!/usr/bin/env python3
"""Translate SRT cues with a local Ollama model while preserving timestamps."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Cue:
    index: int
    start: str
    end: str
    text: str


def read_srt(path: Path) -> list[Cue]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) >= 3 and " --> " in lines[1]:
            start, end = lines[1].split(" --> ", 1)
            cues.append(Cue(int(lines[0]), start, end, " ".join(lines[2:])))
    return cues


def write_srt(path: Path, cues: list[Cue]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n\n".join(
            f"{cue.index}\n{cue.start} --> {cue.end}\n{cue.text}" for cue in cues
        )
        + "\n",
        encoding="utf-8",
    )


def load_glossary(path: Path | None) -> str:
    if not path:
        return ""
    data = path.read_text(encoding="utf-8").strip()
    return f"\nFollow this glossary exactly:\n{data}\n" if data else ""


def translate_chunk(args: argparse.Namespace, cues: list[Cue], glossary: str) -> dict[int, str]:
    items = [{"id": cue.index, "text": cue.text} for cue in cues]
    prompt = f"""
Translate these {args.source_language} podcast subtitle cues into natural, concise
{args.target_language}. Preserve meaning, uncertainty, opinion qualifiers, names,
and technical terminology. Do not summarize, merge, omit, censor, or add facts.
Keep every translation short enough for subtitles.{glossary}

Return JSON only in this shape:
{{"translations":[{{"id":1,"text":"translated subtitle"}}]}}

Input cues:
{json.dumps(items, ensure_ascii=False)}
"""
    schema = {
        "type": "object",
        "properties": {
            "translations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"id": {"type": "integer"}, "text": {"type": "string"}},
                    "required": ["id", "text"],
                },
            }
        },
        "required": ["translations"],
    }
    payload = json.dumps(
        {
            "model": args.model,
            "stream": False,
            "format": schema,
            "messages": [{"role": "user", "content": prompt}],
            "options": {"temperature": args.temperature, "num_ctx": args.num_ctx},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        args.endpoint.rstrip("/") + "/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=args.timeout) as response:
        envelope = json.loads(response.read().decode("utf-8"))
    content = json.loads(envelope["message"]["content"])
    return {int(item["id"]): item["text"].strip() for item in content["translations"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL"))
    parser.add_argument("--endpoint", default=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"))
    parser.add_argument("--source-language", default="the source language")
    parser.add_argument("--target-language", default="English")
    parser.add_argument("--glossary", type=Path)
    parser.add_argument("--chunk-size", type=int, default=50)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--num-ctx", type=int, default=8192)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    if not args.model:
        parser.error("provide --model or set OLLAMA_MODEL")

    cues = read_srt(args.source)
    glossary = load_glossary(args.glossary)
    partial = args.destination.with_suffix(args.destination.suffix + ".partial.json")
    translated: dict[int, str] = {}
    if partial.exists():
        translated.update({int(key): value for key, value in json.loads(partial.read_text()).items()})

    def save(result: dict[int, str]) -> None:
        translated.update(result)
        partial.write_text(json.dumps(translated, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Translated {len(translated)}/{len(cues)} cues", flush=True)

    def process(group: list[Cue]) -> None:
        if not group:
            return
        error: Exception | None = None
        for _ in range(2):
            try:
                result = translate_chunk(args, group, glossary)
                missing = {cue.index for cue in group} - result.keys()
                if missing:
                    raise ValueError(f"Model omitted cue IDs: {sorted(missing)}")
                save(result)
                return
            except Exception as exc:
                error = exc
                time.sleep(2)
        if len(group) == 1:
            raise RuntimeError(f"Unable to translate cue {group[0].index}") from error
        midpoint = len(group) // 2
        process(group[:midpoint])
        process(group[midpoint:])

    for offset in range(0, len(cues), args.chunk_size):
        process([cue for cue in cues[offset : offset + args.chunk_size] if cue.index not in translated])

    write_srt(
        args.destination,
        [Cue(cue.index, cue.start, cue.end, translated[cue.index]) for cue in cues],
    )


if __name__ == "__main__":
    main()
