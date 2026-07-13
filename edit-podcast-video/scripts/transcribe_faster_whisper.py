#!/usr/bin/env python3
"""Transcribe media with faster-whisper and write SRT plus JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def srt_timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def word_payload(word: Any) -> dict[str, Any]:
    return {
        "start": getattr(word, "start", None),
        "end": getattr(word, "end", None),
        "word": getattr(word, "word", ""),
        "probability": getattr(word, "probability", None),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video with faster-whisper to SRT and JSON."
    )
    parser.add_argument("input", type=Path, help="Input audio or video file")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output-stem", help="Output basename; defaults to input stem")
    parser.add_argument("--model", default="large-v3", help="Model name or local model path")
    parser.add_argument("--language", help="BCP-47-like language code, e.g. zh or en")
    parser.add_argument("--device", default="cpu", choices=("cpu", "cuda", "auto"))
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--vad-filter", action="store_true")
    parser.add_argument("--word-timestamps", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        raise SystemExit(f"Input file not found: {args.input}")

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit(
            "faster-whisper is not installed. Run: pip install faster-whisper"
        ) from exc

    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = args.output_stem or args.input.stem
    srt_path = args.output_dir / f"{stem}.srt"
    json_path = args.output_dir / f"{stem}.json"

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
    )
    segment_stream, info = model.transcribe(
        str(args.input),
        language=args.language,
        beam_size=args.beam_size,
        vad_filter=args.vad_filter,
        word_timestamps=args.word_timestamps,
    )
    segments = list(segment_stream)

    srt_blocks: list[str] = []
    json_segments: list[dict[str, Any]] = []
    for index, segment in enumerate(segments, start=1):
        text = segment.text.strip()
        srt_blocks.append(
            f"{index}\n{srt_timestamp(segment.start)} --> "
            f"{srt_timestamp(segment.end)}\n{text}"
        )
        item: dict[str, Any] = {
            "id": getattr(segment, "id", index - 1),
            "start": segment.start,
            "end": segment.end,
            "text": text,
            "avg_logprob": getattr(segment, "avg_logprob", None),
            "no_speech_prob": getattr(segment, "no_speech_prob", None),
        }
        words = getattr(segment, "words", None)
        if words is not None:
            item["words"] = [word_payload(word) for word in words]
        json_segments.append(item)

    srt_path.write_text("\n\n".join(srt_blocks) + "\n", encoding="utf-8")
    payload = {
        "input": str(args.input),
        "model": args.model,
        "device": args.device,
        "compute_type": args.compute_type,
        "language": getattr(info, "language", args.language),
        "language_probability": getattr(info, "language_probability", None),
        "duration": getattr(info, "duration", None),
        "duration_after_vad": getattr(info, "duration_after_vad", None),
        "segments": json_segments,
    }
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(srt_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
