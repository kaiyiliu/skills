# Local model routes

Use this reference only when the user requests local/offline processing or no hosted transcription/translation function is available. Do not copy model weights, virtual environments, caches, or raw user media into the skill.

## Speech-to-text with faster-whisper

`SYSTRAN/faster-whisper` is the preferred local transcription route. It runs Whisper models through CTranslate2, supports CPU quantization and NVIDIA CUDA, and can emit word timestamps. The bundled wrapper writes both SRT and machine-readable JSON.

```bash
python3 -m venv work/faster-whisper-venv
work/faster-whisper-venv/bin/pip install faster-whisper
work/faster-whisper-venv/bin/python scripts/transcribe_faster_whisper.py \
  current/episode.mp4 \
  --output-dir work/transcript \
  --model large-v3 \
  --language zh \
  --device cpu \
  --compute-type int8 \
  --vad-filter \
  --word-timestamps
```

For a compatible NVIDIA GPU, use `--device cuda --compute-type float16`. CPU `int8` is the portable default. The wrapper intentionally avoids guessing a GPU route.

Run the wrapper with `--help` before use. Model identifiers are examples, not bundled dependencies. Loading a model name such as `large-v3` can download its CTranslate2 weights from Hugging Face on the first run; request approval before network access. A local converted-model directory can be passed to `--model` for offline use.

For lower-memory machines, choose a smaller model. Always proofread names, quotations, dates, numbers, and specialized terminology. Preserve the generated JSON alongside the SRT so later editorial steps can trace timestamps and confidence-related metadata.

Official reference: <https://github.com/SYSTRAN/faster-whisper>

## Subtitle translation with Ollama

The bundled `scripts/srt_translate_ollama.py` calls the local Ollama chat endpoint and requests structured JSON. It requires a running Ollama service and a locally available model:

```bash
ollama serve
ollama pull <model-name>
python scripts/srt_translate_ollama.py \
  output/captions.zh-Hans.srt \
  output/captions.en.srt \
  --model <model-name> \
  --source-language "Simplified Chinese" \
  --target-language "English" \
  --glossary work/glossary.txt
```

The script saves a partial JSON checkpoint beside the destination and retries smaller groups when a model omits cue IDs. A successful structured response does not prove translation quality; require human review for names, quotations, legal statements, and technical terminology.

Official references: <https://github.com/ollama/ollama>, <https://github.com/ollama/ollama/blob/main/docs/api.md>

## Privacy and reproducibility

- Keep models and caches outside the public skill directory.
- Do not commit `.venv/`, model weights, raw transcripts, media, or partial translations.
- Record model name, language, major options, and whether the run was local or hosted in the episode log.
- Treat downloaded models as third-party software with their own licenses.
