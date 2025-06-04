"""Animation utilities."""
import logging
from pathlib import Path

import subprocess


def animate_image(image_path: Path, audio_path: Path, result_dir: Path) -> Path:
    """Use SadTalker to animate an image based on speech audio."""
    logging.info("Animating %s with SadTalker", image_path)
    try:
        subprocess.run([
            "sadtalker",
            "--driven_audio",
            str(audio_path),
            "--source_image",
            str(image_path),
            "--result_dir",
            str(result_dir),
        ], check=True)
        gen = result_dir / "results" / "driven_audio" / image_path.stem / "result.mp4"
        if gen.exists():
            return gen
    except Exception as e:
        logging.warning("SadTalker failed: %s", e)
    return image_path
