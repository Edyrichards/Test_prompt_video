# Test Prompt Video


This repository contains a modular pipeline to generate a one‑minute video from a text prompt using only open‑source tools. It is designed to run locally on macOS with Apple Silicon.

## Setup

```bash
bash setup_macos.sh
```

This creates a Python virtual environment, installs PyTorch with MPS support, and downloads required packages.

## Usage

Run the CLI:

```bash
python main.py --prompt "A hero's journey" --emotion inspirational --style pixar --speaker tts_models/en/vctk/vits --music auto --animate --output final.mp4
```

### CLI Options
- `--prompt` – text prompt
- `--emotion` – emotion context (default `happy`)
- `--style` – image style preset (`anime`, `pixar`, `realistic`)
- `--speaker` – TTS voice or speaker file
- `--lora` – path to LoRA weights for Stable Diffusion
- `--music` – `auto` to generate with MusicGen or path to an mp3
- `--animate` – enable SadTalker animation
- `--output` – output mp4 file

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
