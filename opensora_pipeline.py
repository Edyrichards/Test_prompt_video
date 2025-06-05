"""CLI wrapper around Open-Sora for text-to-video generation."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from core.open_sora import generate_video


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate video using Open-Sora")
    p.add_argument("--prompt", required=True, help="Text prompt for the video")
    p.add_argument(
        "--opensora-dir",
        default=str(Path.home() / "Open-Sora"),
        help="Path to the cloned Open-Sora repository",
    )
    p.add_argument(
        "--resolution",
        default="256px",
        choices=["256px", "768px"],
        help="Generation resolution",
    )
    p.add_argument("--offload", action="store_true", help="Enable CPU offloading")
    p.add_argument("--save-dir", default="samples", help="Directory to save results")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    opensora_dir = Path(args.opensora_dir).expanduser()
    save_dir = Path(args.save_dir).expanduser()
    save_dir.mkdir(parents=True, exist_ok=True)

    generate_video(
        prompt=args.prompt,
        opensora_dir=opensora_dir,
        save_dir=save_dir,
        resolution=args.resolution,
        offload=args.offload,
    )

    logging.info("Video saved under %s", save_dir)


if __name__ == "__main__":  # pragma: no cover
    main()
