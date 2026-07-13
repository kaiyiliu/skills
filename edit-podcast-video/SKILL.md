---
name: edit-podcast-video
description: Edit audio or video podcast recordings through transcript-led cuts, two user-editable Markdown plans, cold-open highlights and music, dialogue repair, multilingual subtitle files, mastering, holistic AI review, and platform publishing metadata. Use for MP4, MOV, MKV, WAV, M4A, MP3, reference episodes, and podcast release packages. Route video sources to audio-led or full-visual editing; route audio-only sources to podcast delivery without YouTube or Xiaohongshu assets.
---

# Edit Podcast Audio or Video

Preserve source media. Use editable Markdown as the control plane; the user's latest saved documents override earlier proposals and chat summaries.

## Runtime dependencies and callable tools

Check these at the start and use only what the selected route needs:

- Required media tools: `ffmpeg`, `ffprobe`, and a callable shell such as `exec_command`.
- Required file operations: file search/read plus `apply_patch` or an equivalent safe write call.
- Required transcription route: preferably the bundled `faster-whisper` wrapper for local work, another installed speech-to-text engine, an available transcription function/API, or a user-provided transcript.
- Optional inspection: `view_image`, frame extraction, waveform/spectrogram tools, and loudness analysis.
- Optional language route: a local model or available translation function for multilingual captions; always flag machine translation for human review.
- Optional visual route: an authorized Google Photos/Drive connector, licensed media search, HTML/canvas workflow, `image_gen.imagegen`, or an available video-generation function. Discover connector/generator calls through the current tool registry; use them only in `full-visual` mode and only after authorization.
- Optional finishing: a native NLE plus EDL/XML/FCPXML/Resolve handoff when manual finishing is useful.
- Missing software or connectors: use the environment's approval/escalation call or plugin-install request before installation, download, connector use, or media generation.

Record the tools actually used and distinguish automated checks from actual watching/listening.

## Bundled reusable resources

- Copy blank control documents from `assets/templates/` instead of recreating their schemas.
- Read [references/local-models.md](references/local-models.md) only for local/offline transcription or subtitle translation.
- Use `scripts/transcribe_faster_whisper.py` for local transcription. Use `scripts/srt_merge_cues.py`, `scripts/srt_translate_ollama.py`, `scripts/srt_bilingual.py`, `scripts/srt_remap_timeline.py`, and `scripts/srt_to_markdown.py` for their named deterministic operations. Run `--help` first and preserve user-edited subtitle files.

## Route by source

- `video + audio-led`: decide cuts from dialogue and sound. Apply every cut at identical audio/video boundaries. Do not add independent picture edits.
- `video + full-visual`: allow approved multicam, reframing, graphics, or B-roll with source and rights records.
- `audio-only`: edit and master the podcast audio. Skip video planning, video exports, YouTube copy, Xiaohongshu copy, and all visual deliverables. Create podcast-feed metadata only when publishing materials are requested.

Prefer FFmpeg for deterministic edits and a native NLE for complex manual visual finishing. Never claim to have watched or heard media unless it was decoded and inspected.

## Stage 0: fast preflight and brief

1. Read the applicable guide: [references/editing-guide.md](references/editing-guide.md), or [references/editing-guide.zh-CN.md](references/editing-guide.zh-CN.md) for Chinese work.
2. Inventory only relevant source, reference, music, and delivery files. Record codecs, duration, resolution/frame rate for video, sample rate/channels, and measurable loudness.
3. Create or refresh `output/episode-brief.md` from `assets/templates/episode-brief.md`. Require only the core purpose; source type; processing route; exclusions; target platforms/duration; references; subtitle languages/formats; and other non-negotiables. Do not require intended audience effect, desired tone, or must-keep material.
4. Ask only for information that blocks an editorial or rights decision. Infer safe technical defaults and record them instead of adding approval steps.

## Stage 1: Round 1 content plan

1. Transcribe with timestamps and speaker labels; mark uncertain words rather than guessing.
2. Analyze reference episodes only when supplied, and only for the requested attributes.
3. Identify story structure, strong answers, repetition, false starts, long pauses, tangents, sensitive passages, technical faults, and candidate short clips.
4. Propose a cold-open highlight montage after analyzing the full recording. Use complete statements, source timecodes, assembly order, duration, and context risk. Do not manufacture a claim by splicing clauses.
5. Add a separate cold-open music brief. First inspect user-provided candidates in `assets/`; otherwise propose licensed/user-provided acquisition or an authorized generation route. Keep cold-open, intro, chapter, and outro music as separate decisions even when they reuse a track.
6. Write `output/round-1-content-plan.md`, `output/transcript.md`, and `output/subtitle-plan.md`, using bundled templates where applicable. Create `output/reference-style.md` only when a reference is supplied.

## Stage 2: Round 2 timeline plan

1. Re-read the latest brief and Round 1 plan.
2. For `audio-only`, map audio cuts, music, captions/transcript, and exports; omit all visual columns.
3. For `video + audio-led`, map approved audio cuts to identical video cuts; state that independent picture edits are not authorized.
4. For `video + full-visual`, record every insert's source time, timeline position, duration, placement, entrance/exit, audio behavior, purpose, source, rights, and approval.
5. Write `output/round-2-timeline-plan.md`, `output/music-plan.md`, and `output/asset-log.md` only to the detail needed by assets actually used.

For simple or audio-led work, generate both round documents in one pass and use one combined approval gate. Stop separately only when a substantive cut, sensitive passage, external asset, new music, or generation choice needs a user decision.

## Stage 3: render and revise

1. Apply only approved substantive edits. Remove clear false starts and duplicate takes while retaining natural breath, laughter, emotion, and conversational rhythm.
2. Repair dialogue conservatively. Avoid metallic denoising artifacts and over-compression.
3. Use music sparingly and duck it under speech. Confirm rights for user-provided `assets/` tracks before publication.
4. Generate each requested subtitle format and language. Burn captions only when requested.
5. Render a low-cost preview for nontrivial or uncertain edits. When the plan is deterministic and explicitly approved, proceed directly to a delivery render and QC to save time.
6. Record changes in `output/edit-log-v1.md`; keep prior versions.

## Stage 4: review, master, and package

1. Inspect the actual media sequentially. Check sync when video exists, clipped words, abrupt cuts, silence, audio artifacts, peaks, caption timing, spelling, translation, music transitions/rights, and end padding.
2. Create `output/ai-final-review.md`; separate objective defects from subjective suggestions. Do not apply new subjective edits without approval.
3. Export the approved route:
   - video source: final video plus WAV and compressed podcast audio;
   - audio-only source: WAV master plus MP3/M4A, with no video deliverables.
4. Default podcast loudness only when no house standard exists: about -16 LUFS stereo or -19 LUFS mono, true peak at or below -1 dBTP. Measure it.
5. Generate publishing materials only for requested platforms. For audio-only input, generate podcast-feed title, summaries, chapters, tags/categories, credits, and manifest; never generate YouTube or Xiaohongshu assets.
6. Validate media/subtitle paths, JSON, chapters, names, and factual claims. Create `output/qc-report.md`.

## Editorial guardrails

- Never change a speaker's meaning through deletion or reordered fragments.
- Flag legal, confidential, controversial, or reputational material for explicit approval.
- Never fabricate reaction shots, events, product screens, quotations, or evidence.
- Label synthetic illustrative media when it could be mistaken for documentary evidence.
- Require a human full-length review before publication.
