Create the virtual environment and install dependencies. The setup script
installs PyTorch first so that packages like `xformers` compile correctly.

This repository contains a modular pipeline to generate a **1-minute video** from a **text prompt**, entirely offline, using only **open-source tools**. It runs locally on **macOS (Apple Silicon)** and handles scriptwriting, image generation, voice synthesis, optional animation, and video assembly.

---

## ✨ Features

- 🎬 Emotion-aware script generation using LLMs (e.g. Mistral-7B)
- 🎨 Style-specific images via Stable Diffusion with optional LoRA
- 👄 Optional lipsync animation using SadTalker
- 🗣 Expressive voice-over with Coqui TTS or Bark
- 🎵 Automatic or custom background music using MusicGen
- 🧩 Crossfades and zoom effects with MoviePy
- 🔒 100% local – no API keys required after model download

---

## 🖥 Requirements

- macOS 12+ with Apple Silicon (M1/M2)
- Python 3.10 or newer
- At least 16 GB RAM recommended
- ~15 GB free disk space for cached models

---

## 🔧 Setup

This sets up a virtual environment, installs dependencies (with MPS support for Mac GPU), and prepares models for local inference:

```bash
bash setup_macos.sh
source venv/bin/activate
```

---

## 🚀 Usage

Example command to generate an inspirational Pixar-style clip:

```bash
python main.py \
  --prompt "a boy overcomes fear" \
  --emotion inspirational \
  --style pixar \
  --speaker tts_models/en/vctk/vits \
  --music auto \
  --animate \
  --output final_video.mp4
```

---

## 🛠 CLI Flags

| Flag          | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `--prompt`    | Main text prompt/theme for the video                                        |
| `--emotion`   | Emotional tone (`happy`, `sad`, `inspirational`, etc.)                      |
| `--style`     | Visual style: `anime`, `pixar`, `realistic`                                 |
| `--speaker`   | Coqui TTS model ID or custom speaker file                                   |
| `--lora`      | Path to a LoRA weights file for Stable Diffusion                            |
| `--music`     | `auto` (MusicGen) or path to a local `.mp3` file                            |
| `--animate`   | Enables SadTalker-based talking animation                                   |
| `--output`    | Output video filename (e.g., `final.mp4`)                                   |

---

## 🧩 Pipeline Components

1. **Script Generator** – Mistral‑7B‑Instruct (`transformers`)
2. **Image Generator** – Stable Diffusion (`diffusers`) with style and LoRA support
3. **Animation Engine** – SadTalker for lipsync; fallback to Ken Burns zoom
4. **Voice Synthesizer** – Coqui TTS or Bark with emotional tone
5. **Music Composer** – Audiocraft MusicGen or user-provided track
6. **Video Editor** – `moviepy` for fade effects, zoom, and audio sync

---

## ✅ Testing

Run static code checks and test the pipeline:

```bash
python -m py_compile $(find . -name '*.py')
python test_pipeline.py
```

---

## 🌟 Preview

> *(Add a sample output GIF or YouTube link here)*

---

## 📄 License

MIT – Fully open-source and free for personal or commercial use.

---

## 📬 Contribute or Reach Out

Feel free to open an issue, fork the repo, or contribute enhancements. Let’s make AI storytelling accessible to everyone 🎬✨
