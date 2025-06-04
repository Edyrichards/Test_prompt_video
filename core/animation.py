"""Animation utilities."""
import logging
from pathlib import Path

import subprocess


def animate_image(image_path: Path, audio_path: Path, result_dir: Path) -> Path:
    """Use SadTalker to animate an image based on speech audio."""
    logging.info("Animating %s with SadTalker", image_path)
    sadtalker_python = Path.home() / "SadTalker" / "venv" / "bin" / "python"
    sadtalker_wrapper = Path.home() / "SadTalker" / "sadtalker_cli.py"
    cmd = [
        str(sadtalker_python),
        str(sadtalker_wrapper),
        "--source_image",
        str(image_path),
        "--driven_audio",
        str(audio_path),
        "--result_dir",
        str(result_dir),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("SadTalker failed with code %s", e.returncode)
        logging.error("stdout:\n%s", e.stdout)
        logging.error("stderr:\n%s", e.stderr)
        try:
            log_file = result_dir / "sadtalker_error.log"
            log_file.write_text(f"STDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}\n")
            logging.info("Saved SadTalker error log to %s", log_file)
        except Exception as log_exc:  # pragma: no cover - logging failure shouldn't crash
            logging.warning("Failed to write error log: %s", log_exc)
        return image_path
    gen = result_dir / "results" / "driven_audio" / image_path.stem / "result.mp4"
    if gen.exists():
        return gen
    logging.warning("SadTalker output missing: %s", gen)
    return image_path
