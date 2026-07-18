# Edit Podcast Video

[English](#english) · [中文](#中文)

## English

A Codex skill for transcript-led audio and video podcast editing. It uses two user-editable Markdown plans to control content decisions and timeline operations, then produces route-appropriate masters, multilingual subtitles, self-media cover art, QC reports, and publishing metadata. When visual references exist in `assets/`, cover art follows their style.

### Install

Ask Codex to install it from GitHub:

```text
Use $skill-installer to install https://github.com/kaiyiliu/skills/tree/main/edit-podcast-video
```

Or install it manually:

```bash
git clone --depth 1 https://github.com/kaiyiliu/skills.git
mkdir -p ~/.codex/skills
cp -R skills/edit-podcast-video ~/.codex/skills/
```

Restart Codex after installation so it discovers the skill.

### Requirements

- Required: `ffmpeg`, `ffprobe`, and Python 3.
- Transcription: bundled faster-whisper wrapper, another speech-to-text service, or a user-provided transcript.
- Optional: Ollama for local subtitle translation and authorized media/generation tools for full-visual editing.

For local transcription:

```bash
python3 -m venv work/faster-whisper-venv
work/faster-whisper-venv/bin/pip install faster-whisper
work/faster-whisper-venv/bin/python \
  ~/.codex/skills/edit-podcast-video/scripts/transcribe_faster_whisper.py \
  episode.mp4 --output-dir work/transcript --language zh \
  --device cpu --compute-type int8 --vad-filter --word-timestamps
```

### Use

Put source media and optional references/music in an episode folder, then ask Codex:

```text
Use $edit-podcast-video to edit this podcast. Keep all editorial decisions in the two Markdown plans for my review before rendering. Generate Simplified Chinese, English, and bilingual SRT files.
```

The skill routes input automatically:

- `video + audio-led`: edit from dialogue/audio and keep audio/video cut boundaries identical.
- `video + full-visual`: allow approved B-roll, graphics, reframing, or multicam work.
- `audio-only`: export podcast audio and podcast metadata without YouTube or Xiaohongshu video deliverables; create a requested self-media cover when publishing materials are needed.

The original media remains unchanged. Human full-length review is required before publication.

### Documentation

- Runtime instructions: [SKILL.md](SKILL.md)
- Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)
- Editing guide: [references/editing-guide.md](references/editing-guide.md)
- 中文剪辑指南：[references/editing-guide.zh-CN.md](references/editing-guide.zh-CN.md)
- Local models: [references/local-models.md](references/local-models.md)

## 中文

这是一个通过逐字稿驱动播客音视频剪辑的 Codex Skill。它使用两份用户可编辑的 Markdown 文档分别控制内容决策和时间线操作，随后生成对应路线需要的母版、多语言字幕、自媒体封面、质检报告和发布资料。若 `assets/` 中存在视觉参考，封面会遵循其风格。

### 安装

让 Codex 直接从 GitHub 安装：

```text
使用 $skill-installer 安装 https://github.com/kaiyiliu/skills/tree/main/edit-podcast-video
```

也可以手动安装：

```bash
git clone --depth 1 https://github.com/kaiyiliu/skills.git
mkdir -p ~/.codex/skills
cp -R skills/edit-podcast-video ~/.codex/skills/
```

安装后重启 Codex，使其重新发现该 skill。

### 依赖

- 必需：`ffmpeg`、`ffprobe` 和 Python 3。
- 转写：内置 faster-whisper 包装脚本、其他语音转写服务，或用户提供的逐字稿。
- 可选：使用 Ollama 本地翻译字幕；full-visual 路线可使用已经授权的媒体连接器或生成工具。

本地转写命令见上方英文示例，也可阅读 [本地模型说明](references/local-models.md)。

### 使用

把原始媒体和可选的参考节目、音乐放入单集文件夹，然后告诉 Codex：

```text
调用 $edit-podcast-video 剪辑这个播客。渲染前，把所有内容判断写入两轮 Markdown 方案供我修改确认，并生成简体中文、英文和双语 SRT。
```

Skill 会自动选择处理路线：

- `视频 + audio-led`：只根据对白和声音剪辑，音视频使用完全相同的剪切边界。
- `视频 + full-visual`：可以加入已经批准的 B-roll、图形、重构图或多机位剪辑。
- `纯音频`：只输出播客音频和播客发布资料，不生成 YouTube 或小红书视频素材；如需发布资料，可制作已要求的自媒体封面。

原始媒体始终保持不变。发布前仍需人工完整观看或试听。

### 文档

- Codex 执行入口：[SKILL.md](SKILL.md)
- Skill 中文版：[SKILL.zh-CN.md](SKILL.zh-CN.md)
- 中文剪辑指南：[references/editing-guide.zh-CN.md](references/editing-guide.zh-CN.md)
- 本地模型说明：[references/local-models.md](references/local-models.md)

## License

MIT
