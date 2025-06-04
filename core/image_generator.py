"""Image generation and animation using Stable Diffusion and LoRA."""
import logging
from pathlib import Path
from typing import Optional

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

STYLE_MODELS = {
    "pixar": "nerijs/pixart-alpha",
    "anime": "Linaqruf/anything-v3.0",
    "realistic": "runwayml/stable-diffusion-v1-5",
}


def load_pipeline(style: str) -> StableDiffusionPipeline:
    model_name = STYLE_MODELS.get(style, STYLE_MODELS["realistic"])
    logging.info("Loading diffusion model %s", model_name)
    pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )
    pipe.to(device)
    return pipe


def generate_image(prompt: str, emotion: str, style: str, lora: Optional[str] = None) -> Image.Image:
    pipe = load_pipeline(style)
    if lora:
        logging.info("Loading LoRA weights %s", lora)
        pipe.load_lora_weights(lora)
        pipe.fuse_lora()
    formatted = f"{prompt}, dreamy, {emotion}, ultra-detailed"
    logging.info("Generating image with prompt: %s", formatted)
    image = pipe(formatted).images[0]
    return image
