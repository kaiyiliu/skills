# Podcast editing guide

## Folders

```text
reference/   optional published references
current/     source video/audio and intro/outro
assets/      user-provided or approved music, stills, B-roll, logos, fonts
work/        transcripts, proxies, caches, timelines
output/      editable plans, previews, masters, captions, logs, publishing metadata
```

Start control documents from `assets/templates/`. For local/offline processing, read `references/local-models.md`; model weights and episode media remain outside the skill.

## Minimal episode brief

Create `output/episode-brief.md`:

```markdown
# Episode brief

- Core purpose:
- Source type: video / audio-only
- Processing route: audio-led / full-visual / audio-only
- Topics or treatments to avoid:
- Target platforms and duration:
- Reference episodes and attributes to imitate:
- Subtitle/transcript languages:
- Delivery per language: SRT / VTT / burned-in / transcript only
- Other non-negotiables:
```

Only `Core purpose` is editorially required. Ask about other fields only when missing information blocks a decision. Do not require intended audience effect, desired tone, or must-keep material.

## Source routing

| Source | Planning | Media output | Publishing package |
|---|---|---|---|
| Video, audio-led | Dialogue-led cuts; identical video/audio boundaries | final video + WAV + MP3/M4A | requested video platforms + podcast |
| Video, full-visual | Dialogue edit plus approved visual timeline | final video + WAV + MP3/M4A | requested video platforms + podcast |
| Audio-only | Audio cuts, repair, music, transcript/captions | WAV + MP3/M4A | podcast feed only; no YouTube/Xiaohongshu |

## Round 1: content plan

Use one row per editorial decision:

| ID | Source time | Timeline position | Action | Transcript/reason | Meaning risk | Approval |
|---|---|---|---|---|---|---|
| E001 | 00:04:12–00:04:20 | after opening | Shorten pause | repeated setup | none | approved |

Mark sensitive, uncertain, reordered, or meaning-changing edits `needs-user`.

### Cold-open montage

Analyze the full recording first. When the material supports it, include two or three concepts with source timecodes, verbatim excerpts, order, total duration, transition gaps, and context risk. Use complete statements and preserve qualifiers.

| Clip | Source time | Verbatim excerpt | Order | Role | Context risk | Approval |
|---|---|---|---|---|---|---|
| H001 | 00:22:00–00:22:07 | “...” | 1 | establish hook | low | needs-user |

For video `audio-led`, use each clip's linked original picture. For audio-only, create an audio montage only.

### Separate cold-open music brief

Track cold-open music separately from intro, chapter, and outro. Record role, mood/energy, approximate tempo, texture, lyric policy, duration, start/end, speech ducking, source, rights, and approval.

Source priority:

1. suitable user-provided music already in `assets/`;
2. another user-provided or clearly licensed track;
3. authorized original generation.

Round 1 may name an `assets/` candidate and its intended excerpt. Do not generate or download new music without approval. Confirm publication rights even for user-provided files.

## Round 2: timeline plan

### Audio-only

| ID | Source time | Timeline position | Audio action | Music/caption note | Approval |
|---|---|---|---|---|---|

### Video, audio-led

| ID | Source A/V time | Timeline position | Audio action | Identical video action | Music/caption note | Approval |
|---|---|---|---|---|---|---|

### Video, full-visual

| ID | Source time | Timeline position | Duration | Placement/transition | Audio behavior | Source/rights | Purpose | Approval |
|---|---|---|---|---|---|---|---|---|

For external visuals, record source, creator, license, attribution, acquisition date, and timeline location. Use private-photo connectors, licensed search, screen recording, AI generation, or HTML animation only when available and authorized.

For simple or audio-led episodes, generate both round documents together and request one combined approval. Add a separate stop only for consequential choices.

## Music and audio

- Use user-provided or clearly licensed music only; document source, license, edit position, fades, and ducking.
- Keep cold-open, intro, chapter, and outro as separate rows even when one track is reused.
- Repair dialogue conservatively; check intelligibility by listening, not waveform alone.
- Default final loudness only when no house standard exists: about -16 LUFS stereo or -19 LUFS mono, true peak at or below -1 dBTP.

## Captions and transcript

Ask which languages and formats are required. Record source/target language, SRT/VTT/burned-in/transcript-only, reading preference, names/terms, and reviewer. Machine translation is not verified translation; flag names, quotations, legal claims, and specialist terms.

Use the bundled SRT scripts for merging short cues, timeline remapping, Ollama translation, bilingual assembly, and timestamped Markdown conversion rather than writing episode-specific utilities.

## Publishing package

Create only requested platform files and one UTF-8 `publish-manifest.json` per approved language.

### Video source

- YouTube when requested: 5 titles, description, verified chapters, tags, hashtags, pinned comment, languages, links, and credits.
- Xiaohongshu when requested: 5 titles, opening hook, skimmable body, CTA, hashtags, and credits.
- Podcast feed when requested: title options, summaries, show notes, chapters, credits, categories, and search keywords.

### Audio-only source

Create podcast-feed materials only. Do not create YouTube or Xiaohongshu files, thumbnail text, video chapters, or visual assets.

Base every claim on the approved timeline, transcript, brief, and verified guest information. Use `null` or `needs_user` rather than inventing missing facts.

## Review and delivery

1. Inspect the actual media sequentially.
2. Separate objective defects from subjective suggestions in `output/ai-final-review.md`.
3. Validate cuts, sync when applicable, silence, peaks, captions, translations, music rights/transitions, chapters, JSON, and relative paths.
4. State which checks were automated and which were verified by watching/listening.

Deliver only route-relevant files: final media, requested captions/transcript, brief, two round plans, edit/music/asset logs as applicable, AI review, QC report, and requested publishing metadata. No cover plan or cover artwork is required.
