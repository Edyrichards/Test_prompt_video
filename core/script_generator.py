"""Script generation module."""
import logging
from typing import List

from transformers import pipeline


def generate_script(prompt: str, emotion: str, model: str = "mistralai/Mistral-7B-Instruct") -> List[str]:
    """Generate six short script segments using a large language model."""
    logging.info("Generating script with model %s", model)
    text_gen = pipeline("text-generation", model=model, device_map="auto")
    base_prompt = (
        f"Write a cinematic six part script for a one minute video about: {prompt}. "
        f"Each part should be roughly ten seconds long and convey a {emotion} tone."
    )
    output = text_gen(base_prompt, max_new_tokens=200, do_sample=True)[0]["generated_text"]
    sentences = [s.strip() for s in output.split("\n") if s.strip()]
    if len(sentences) < 6:
        sentences = [s.strip() for s in output.split(".") if s.strip()]
    if len(sentences) < 6:
        sentences += ["..."] * (6 - len(sentences))
    return sentences[:6]
