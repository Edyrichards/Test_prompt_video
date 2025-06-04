# 🎞️ Open Source Video Generator

Generate a one-minute video from a text prompt entirely offline on macOS using open-source tools only. The pipeline orchestrates script writing, image creation, animation, voice synthesis and final assembly on Apple Silicon machines.
## ✨ Features
- Emotion-aware script generation with large language models
- Style specific images via Stable Diffusion with optional LoRA
- Optional lipsync animation using SadTalker
- Expressive voice over with Coqui TTS
- Automatic or custom background music using Audiocraft MusicGen
- Crossfades and zoom effects during video assembly
- Runs locally with no API keys once models are downloaded

## 🖥 Requirements
- macOS 12+ on Apple Silicon (M1/M2) with at least 16GB RAM
- Python 3.10 or newer
- ~15 GB free disk space for model caches

## 🔧 Setup
Run the setup script to create a virtual environment, install dependencies and enable PyTorch MPS:

Then activate the environment:

```bash
source venv/bin/activate
```
## 🚀 Usage
Generate a Pixar-style inspirational clip:
python main.py --prompt "a boy overcomes fear" --emotion inspirational --style pixar --speaker tts_models/en/vctk/vits --music auto --animate --output final_video.mp4

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

## 🏗 Pipeline Components
1. **Script Generator** – Mistral-7B-Instruct via `transformers`
2. **Image Generator** – Stable Diffusion with style presets and LoRA support
3. **Animation** – SadTalker lipsync or Ken Burns fallback
4. **Voice Synthesizer** – Coqui TTS with emotion tags
5. **Music** – Audiocraft MusicGen or provided track
6. **Video Editor** – MoviePy crossfades, zooms and audio mixing

## ✅ Testing
Compile all Python modules and run the unit tests:
python -m py_compile $(find . -name '*.py')

## 🌟 Preview
> Add a preview GIF here

## ⚖️ License
MIT
## Components
- **Script generation:** Mistral‑7B‑Instruct via `transformers`.
- **Image generation:** Stable Diffusion with optional LoRA.
- **Animation:** SadTalker or Ken Burns effect.
- **Voice:** Coqui TTS with optional speaker.
- **Music:** Audiocraft MusicGen when `--music auto` is used.
- **Video assembly:** moviepy crossfades and zooms.

## Testing

Run a minimal unit test:

```bash
python test_pipeline.py
```

This repository contains a prototype pipeline for generating a 1-minute video from a text prompt using open source tools only. The pipeline is implemented in `video_pipeline.py`.

## Requirements

```bash
bash setup_macos.sh  # creates a venv and installs all deps
```

The dependencies include:
- `transformers` and `torch` for text generation
- `diffusers` for Stable Diffusion image generation
- `tts` (Coqui TTS) or Bark for expressive speech synthesis
- `audiocraft` for background music generation
- `moviepy` and `ffmpeg-python` for video assembly
- `opencv-python` for post-processing

Large models (e.g. Stable Diffusion and TTS models) will be downloaded on first run and require sufficient system resources.

## Usage

```bash
python video_pipeline.py --prompt "A hero's journey" --emotion inspirational --style pixar --voice tts_models/en/vctk/vits --output final.mp4
```

The script will:
1. Generate a short six-part script that reflects the chosen emotion
2. Create an image for each segment using a Stable Diffusion model matching the style
3. Optionally animate the stills with AnimateDiff or SadTalker and lipsync the dialogue
4. Synthesize expressive voice-over audio
5. Generate or use background music that matches the tone
6. Combine images, audio, and music into a polished video with crossfades

The final result is saved to the path specified by `--output`.
 main
