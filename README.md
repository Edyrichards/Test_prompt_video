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
