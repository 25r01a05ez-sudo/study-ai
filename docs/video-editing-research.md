# Video Editing Repositories: Research & Comparison

> **Context:** This document compares four AI-assisted video editing repositories for **general video editing** capability.
>
> Repositories reviewed:
> - [kevinbadi/hyperedit](https://github.com/kevinbadi/hyperedit)
> - [OwlTing/AI_basketball_games_video_editor](https://github.com/OwlTing/AI_basketball_games_video_editor)
> - [poseljacob/agentic-video-editor](https://github.com/poseljacob/agentic-video-editor)
> - [gausian-AI/Gausian_native_editor](https://github.com/gausian-AI/Gausian_native_editor)

---

## 1. kevinbadi/hyperedit (ClipWise / HyperEdit)

**Type:** Browser-based AI video editor  
**Tech Stack:** React 19, Remotion, Cloudflare Workers, local FFmpeg server, Google Gemini 2.5 Flash, fal.ai

### Capabilities
- Multi-track timeline editor with 6 tracks: captions (T1), overlays (V2/V3), base video (V1), and dual audio (A1/A2)
- AI Director agent: interprets natural-language editing commands to trim, arrange, add captions, and generate motion graphics
- Picasso agent: AI image generation via fal.ai
- DiCaprio agent: video generation (image-to-video), video style transfer, and background removal
- Auto-captioning with local Whisper transcription (word-level timestamps)
- 11 built-in Remotion motion-graphics templates (text, data, branding, mockup, etc.)
- AI-generated dynamic animations (Gemini writes JSX → Remotion renders)
- Dead-air removal via FFmpeg silence detection
- GIF creation, GIPHY integration, audio extraction
- Session-based local FFmpeg server for all heavy processing
- Production deployment on Cloudflare Workers + R2 + D1

### General Editing Score: ⭐⭐⭐⭐⭐
**Best choice for general video editing.** Full-featured, browser-based, works with any video content, and combines a traditional multi-track timeline with powerful AI agents. No domain restriction.

---

## 2. OwlTing/AI_basketball_games_video_editor

**Type:** Command-line sports highlight generator  
**Tech Stack:** Python 3.6, PyTorch YOLOv4, OpenCV, TensorRT (optional)

### Capabilities
- Detects basketball and basketball-hoop positions frame-by-frame using YOLOv4 object detection
- Identifies shot frames automatically from object trajectories
- Cuts source footage around detected shot moments and merges into a highlight reel
- Multiple output modes: `full`, `basketball`, `shot`, `standard`, `clean`
- Supports both PyTorch and TensorRT inference engines
- Requires custom-trained YOLOv4 weights (basketball-specific)

### General Editing Score: ⭐☆☆☆☆
**Not suitable for general video editing.** The tool is purpose-built for basketball footage only. It performs no text/audio editing, has no timeline interface, and its AI models are basketball-specific. Using it for non-basketball content would produce no useful output.

---

## 3. poseljacob/agentic-video-editor (AVE)

**Type:** CLI-first agentic video editor  
**Tech Stack:** Python 3.11+, Google Gemini (via ADK), FFmpeg, MoviePy

### Capabilities
- Multi-agent pipeline: **Director → Trim Refiner → Editor → Reviewer**
  - **Director**: searches a footage index, selects shots, writes an `EditPlan` with trims, ordering, and text overlays
  - **Trim Refiner**: tightens shot boundaries
  - **Editor**: renders the `EditPlan` to MP4 via FFmpeg/MoviePy
  - **Reviewer**: scores the output on 5 dimensions (adherence, pacing, visual quality, watchability, overall); loops back to Director if score is below threshold
- YAML-configurable pipeline manifests with retry logic
- Style templates (e.g., DTC 30-second ad structure)
- Automatic scene detection, speech transcription, and footage indexing
- Experimental web UI (AVE Studio): FastAPI + Next.js (pre-alpha, CLI is the recommended path)
- Works with any video content — no domain restriction

### General Editing Score: ⭐⭐⭐⭐☆
**Strong choice for automated general editing**, especially turning raw footage into polished short-form ads or presentations. The agentic retry loop and quality scoring make it ideal for unattended pipeline workflows. Less suited for interactive or manual editing sessions.

---

## 4. gausian-AI/Gausian_native_editor

**Type:** Native desktop video editor  
**Tech Stack:** Rust, egui, wgpu, GStreamer, FFmpeg, SQLite, ComfyUI integration

### Capabilities
- GPU-accelerated preview using WGPU with YUV→RGB shaders
- Multi-track timeline with full drag/trim/snap and project persistence (SQLite)
- Hardware video decoding: VideoToolbox (macOS), GStreamer pipelines (cross-platform)
- Proxy generation with hardware profiles: VideoToolbox ProRes, NVIDIA NVENC, Intel VAAPI, software DNxHR
- Export formats: FCPXML 1.9/1.10, FCP7 XML, EDL, JSON
- Local ComfyUI integration: optional embedded WebView and auto-import of AI-generated outputs
- Screenplay/Storyboard helpers with pluggable LLM providers (OpenAI, etc.)
- CLI for headless operations (analyze, convert, encode)
- Cross-platform: macOS, Windows, Linux
- Roadmap includes LORA creator, advanced color grading, effects/transitions, collaborative editing

### General Editing Score: ⭐⭐⭐⭐☆
**Excellent native desktop editor** for general editing with strong performance characteristics. The GPU-accelerated pipeline and professional export formats (FCPXML/EDL) make it suitable for integration with professional NLE workflows. AI features (ComfyUI, LLM storyboard) are present but optional add-ons rather than first-class editing tools.

---

## Summary Comparison

| Feature | HyperEdit | Basketball Editor | Agentic Video Editor | Gausian Native Editor |
|---|:---:|:---:|:---:|:---:|
| **General Video Editing** | ✅ Full | ❌ Basketball only | ✅ Full | ✅ Full |
| **AI-Assisted Editing** | ✅ Director, Picasso, DiCaprio | ✅ YOLOv4 detection | ✅ 4-agent pipeline | ⚠️ ComfyUI (optional) |
| **Timeline / NLE UI** | ✅ Browser-based | ❌ None | ⚠️ Experimental web UI | ✅ Native desktop |
| **CLI / Automation** | ❌ No headless mode | ✅ CLI only | ✅ Primary interface | ✅ CLI included |
| **Multi-track Audio/Video** | ✅ 6 tracks | ❌ None | ❌ Single-clip output | ✅ Multi-track |
| **Auto-Captions** | ✅ Whisper | ❌ No | ❌ No | ❌ No |
| **Export Formats** | MP4 | MP4 | MP4 | FCPXML, FCP7, EDL, JSON, MP4 |
| **Platform** | Web / Cloudflare | Python CLI | Python CLI | macOS / Windows / Linux |
| **License** | Mocha Platform | Apache 2.0 | MIT | MPL-2.0 |
| **Ease of Setup** | Medium (node + ffmpeg) | Hard (CUDA / TensorRT) | Easy (pip / uv) | Medium (Rust + GStreamer) |

---

## Recommendation for General Video Editing

### 🥇 Best Overall: **kevinbadi/hyperedit (ClipWise)**
The most complete general-purpose AI video editor of the four. It provides an interactive browser-based multi-track timeline combined with three distinct AI agents (Director for editing commands, Picasso for image generation, DiCaprio for video generation/styling). It handles captions, motion graphics, audio splitting, dead-air removal, and style transfers — all without any domain restriction. Ideal for users who want an interactive editing experience with AI assistance.

### 🥈 Runner-up for Automation: **poseljacob/agentic-video-editor**
Best suited for unattended or pipeline-style workflows where you have raw footage and a creative brief and want a finished cut automatically. The self-reviewing retry loop is a unique feature that improves output quality without manual intervention. A good fit if you need to process many clips programmatically.

### 🥉 Runner-up for Desktop/Professional: **gausian-AI/Gausian_native_editor**
The best pick for users who prefer a native desktop experience, need professional export formats (FCPXML for Final Cut Pro, EDL for DaVinci Resolve), or require GPU-accelerated performance for large files. AI features are available via ComfyUI integration but are not its primary differentiator.

### ❌ Not Recommended for General Use: **OwlTing/AI_basketball_games_video_editor**
Purpose-built for basketball highlights only. Should not be considered for general video editing.
