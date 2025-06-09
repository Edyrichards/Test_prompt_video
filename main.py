"""Command line interface for the video generation pipeline."""
import argparse
import logging
from pathlib import Path
import tempfile

from core.script_generator import generate_script
from core.image_generator import generate_image
from core.audio_generator import generate_audio
from core.animation import animate_image
from core.video_editor import assemble_video


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a 1-minute video from a prompt")
    p.add_argument("--prompt", required=True, help="Text prompt for the video")
    p.add_argument("--emotion", default="happy", help="Emotion for the video")
    p.add_argument("--style", default="realistic", help="Visual style preset")
    p.add_argument("--speaker", default=None, help="TTS speaker or model")
    p.add_argument("--lora", default=None, help="LoRA weights for image generation")
    p.add_argument("--music", default="auto", help="'auto' or path to mp3")
    p.add_argument("--animate", action="store_true", help="Enable SadTalker animation")
    p.add_argument("--output", default="output.mp4", help="Output video file")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    logging.info("Arguments: %s", args)

    segments = generate_script(args.prompt, args.emotion)

    images = []
    audios = []

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for idx, segment in enumerate(segments):
            img = generate_image(segment, args.emotion, args.style, args.lora)
            audio = generate_audio(segment, args.emotion, args.speaker, tmpdir)
            if args.animate:
                img_path = tmpdir / f"img_{idx}.png"
                img.save(img_path)
                video = animate_image(img_path, audio, tmpdir)
                images.append(video)
            else:
                images.append(img)
            audios.append(audio)

        if args.music == "auto":
            try:
                from audiocraft.models import MusicGen
                logging.info("Generating background music with MusicGen")
                model = MusicGen.get_pretrained("facebook/musicgen-small")
                music_wave = model.generate([f"{args.emotion} background music"], progress=True)
                music_path = tmpdir / "music.wav"
                model.save_wav(music_wave[0], music_path)
            except Exception as e:
                logging.warning("Music generation failed: %s", e)
                music_path = None
        else:
            music_path = Path(args.music)
        assemble_video(images, audios, music_path, Path(args.output))

    logging.info("Video saved to %s", args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
