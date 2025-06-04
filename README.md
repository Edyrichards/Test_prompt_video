# Test Prompt Video

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
