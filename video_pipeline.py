"""Video generation pipeline using open source libraries.
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Union

from transformers import pipeline
from diffusers import StableDiffusionPipeline
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips, CompositeAudioClip, vfx
import tempfile
import torch
import subprocess

# Optional TTS import
try:
    from TTS.api import TTS
except ImportError:  # pragma: no cover
    TTS = None

def generate_script(prompt: str, emotion: str) -> List[str]:
    """Generate 6 short script segments from a prompt and emotion."""
    text_gen = pipeline("text-generation", model="gpt2")
    base = (
        f"Write a six part script for a one minute video about: {prompt}. "
        f"Each part should be roughly ten seconds long and convey a {emotion} tone."
    )
    output = text_gen(base, max_length=200, num_return_sequences=1)[0]["generated_text"]
    sentences = [s.strip() for s in output.split("\n") if s.strip()]
    if len(sentences) < 6:
        raw = output.replace("\n", " ")
        parts = raw.split('.')
        sentences = ['.'.join(parts[i:i+2]).strip() for i in range(0, len(parts), 2)]
    return sentences[:6]

def generate_image(text: str, style: str) -> Image.Image:
    """Generate an image using Stable Diffusion with style presets."""
    style_map = {
        "pixar": "nerijs/pixart-alpha",
        "anime": "Linaqruf/anything-v3.0",
        "realistic": "runwayml/stable-diffusion-v1-5",
    }
    model_name = style_map.get(style, "runwayml/stable-diffusion-v1-5")
    pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    pipe.to(device)
    image = pipe(f"{text}, style {style}").images[0]
    return image

def animate_image(image_path: Path, audio_path: Path, tmpdir: Path) -> Path:
    """Use SadTalker to generate a talking video from an image and audio if available."""
    try:
        out_path = tmpdir / "animated.mp4"
        subprocess.run([
            "sadtalker",
            "--driven_audio",
            str(audio_path),
            "--source_image",
            str(image_path),
            "--result_dir",
            str(tmpdir),
        ], check=True)
        gen = tmpdir / "results" / "driven_audio" / image_path.stem / "result.mp4"
        if gen.exists():
            return gen
    except Exception:
        pass
    return image_path

def generate_audio(text: str, emotion: str, voice: str, tmpdir: Path) -> Path:
    """Generate speech audio using Coqui TTS or Bark."""
    if TTS is None:
        raise RuntimeError("TTS library not installed")
    tts = TTS(model_name=voice, progress_bar=False)
    audio_path = tmpdir / "speech.wav"
    tts.tts_to_file(text=text, file_path=str(audio_path))
    return audio_path

def assemble_video(images: List[Union[Image.Image, Path]], audios: List[Path], music: Path, out_path: Path):
    """Create a video by combining images, audios and background music."""
    clips = []
    for img, audio in zip(images, audios):
        if isinstance(img, Path) and img.suffix.lower() == ".mp4":
            img_clip = VideoFileClip(str(img)).set_duration(10)
        else:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as fp:
                if isinstance(img, Image.Image):
                    img.save(fp.name)
                else:
                    Image.open(img).save(fp.name)
                img_clip = ImageClip(fp.name).set_duration(10)
                img_clip = img_clip.fx(vfx.zoom_in, 1.1)
        img_clip = img_clip.fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5)
        audio_clip = AudioFileClip(str(audio)).set_duration(10)
        clips.append(img_clip.set_audio(audio_clip))
    video = concatenate_videoclips(clips, method="compose", padding=-1, is_mask=False)
    if music.exists():
        bgm = AudioFileClip(str(music)).volumex(0.3).audio_loop(duration=video.duration)
        video = video.set_audio(CompositeAudioClip([video.audio, bgm]))
    video.write_videofile(str(out_path), fps=24)

@dataclass
class GenerationOptions:
    prompt: str
    emotion: str = "happy"
    style: str = "anime"
    voice: str = "tts_models/en/vctk/vits"
    music: Path = field(default_factory=lambda: Path("background.mp3"))
    output: Path = field(default_factory=lambda: Path("output.mp4"))
    animate: bool = False

def main(opts: GenerationOptions):
    segments = generate_script(opts.prompt, opts.emotion)
    images = []
    audios = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for i, segment in enumerate(segments):
            img = generate_image(segment, opts.style)
            images.append(img)
            aud = generate_audio(segment, opts.emotion, opts.voice, tmpdir)
            audios.append(aud)
            if opts.animate:
                img_path = tmpdir / f"frame_{i}.png"
                img.save(img_path)
                anim_path = animate_image(img_path, aud, tmpdir)
                if anim_path.suffix == ".mp4":
                    images[-1] = anim_path
        assemble_video(images, audios, opts.music, opts.output)
    print(f"Video saved to {opts.output}")

if __name__ == "__main__":  # pragma: no cover
    import argparse
    parser = argparse.ArgumentParser(description="Generate a 1-minute video from a prompt")
    parser.add_argument("prompt", help="Text prompt for the video")
    parser.add_argument("--emotion", default="happy", help="Emotion for the video")
    parser.add_argument("--style", default="anime", help="Visual style")
    parser.add_argument("--voice", default="tts_models/en/vctk/vits", help="Coqui TTS voice model")
    parser.add_argument("--music", default="background.mp3", help="Background music file")
    parser.add_argument("--animate", action="store_true", help="Animate images with SadTalker")
    parser.add_argument("--output", default="output.mp4", help="Output video file")
    args = parser.parse_args()
    main(GenerationOptions(prompt=args.prompt, emotion=args.emotion, style=args.style,
                           voice=args.voice, music=Path(args.music), output=Path(args.output),
                           animate=args.animate))
