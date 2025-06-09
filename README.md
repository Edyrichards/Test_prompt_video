# 🎞️ Open Source Video Generator

Generate a one‑minute video from a text prompt entirely offline on macOS using open‑source tools. The pipeline handles script writing, image creation, voice synthesis, optional animation, and final assembly on Apple Silicon machines.

## ✨ Features
- Emotion-aware script generation with large language models
- Style-specific images via Stable Diffusion with optional LoRA
- Optional lipsync animation using SadTalker
- Expressive voice-over with Coqui TTS
- Automatic or custom background music using Audiocraft MusicGen
- Crossfades and zoom effects during video assembly
- Runs locally with no API keys once models are downloaded

## 🖥 Requirements
- macOS 12+ on Apple Silicon (M1/M2) with at least 16 GB RAM
- Python 3.10 or newer
- ~15 GB free disk space for model caches

## 🔧 Setup
Create the virtual environment and install dependencies. The setup script
installs PyTorch first so that packages like `xformers` compile correctly.

```bash
bash setup_macos.sh
source venv/bin/activate
```

## 🚀 Usage
Generate a Pixar-style inspirational clip:

```bash
python main.py --prompt "a boy overcomes fear" --emotion inspirational --style pixar --speaker tts_models/en/vctk/vits --music auto --animate --output final_video.mp4
```

### CLI Flags
| Flag | Description |
|------|-------------|
| `--prompt` | text prompt for the video |
| `--emotion` | emotion context (default `happy`) |
| `--style` | image style preset (`anime`, `pixar`, `realistic`) |
| `--speaker` | TTS voice model or speaker file |
| `--lora` | path to LoRA weights for diffusion |
| `--music` | `auto` to use MusicGen or path to mp3 |
| `--animate` | enable SadTalker animation |
| `--output` | output video path |

## 🏗 Components
1. **Script Generator** – Mistral‑7B‑Instruct via `transformers`
2. **Image Generator** – Stable Diffusion with style presets and LoRA support
3. **Animation** – SadTalker lipsync or Ken Burns fallback
4. **Voice Synthesizer** – Coqui TTS with emotion tags
5. **Music** – Audiocraft MusicGen or provided track
6. **Video Editor** – MoviePy crossfades, zooms and audio mixing

## ✅ Testing
Run static compilation and unit tests:

```bash
python -m py_compile $(find . -name '*.py')
python test_pipeline.py
```

## 🌟 Preview
> Add a preview GIF here

## ⚖️ License
MIT
