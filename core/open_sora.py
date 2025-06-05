"""Wrapper for running Open-Sora text-to-video generation."""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path


def generate_video(
    prompt: str,
    opensora_dir: Path,
    save_dir: Path,
    resolution: str = "256px",
    offload: bool = False,
) -> Path:
    """Run Open-Sora's inference script to create a video.

    Parameters
    ----------
    prompt: str
        The text prompt to generate.
    opensora_dir: Path
        Path to the cloned Open-Sora repository.
    save_dir: Path
        Directory where the results will be written.
    resolution: str
        "256px" or "768px" config to use.
    offload: bool
        Enable CPU offloading during generation.
    """
    config = f"configs/diffusion/inference/t2i2v_{resolution}.py"
    cmd = [
        "torchrun",
        "--nproc_per_node",
        "1",
        "--standalone",
        "scripts/diffusion/inference.py",
        config,
        "--save-dir",
        str(save_dir),
        "--prompt",
        prompt,
    ]
    if offload:
        cmd += ["--offload", "True"]

    logging.info("Running Open-Sora command: %s", " ".join(cmd))
    subprocess.run(cmd, cwd=opensora_dir, check=True)
    return save_dir
