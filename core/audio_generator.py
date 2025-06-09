"""Audio and voice generation module."""
import logging
from pathlib import Path
from typing import Optional

from TTS.api import TTS


def generate_audio(text: str, emotion: str, speaker: Optional[str], tmpdir: Path) -> Path:
    """Generate emotion aware speech audio."""
    model = speaker or "tts_models/en/vctk/vits"
    logging.info("Generating audio with model %s", model)
    tts = TTS(model_name=model, progress_bar=False)
    if not speaker and getattr(tts, "speakers", None):
        speaker = tts.speakers[0]
    tts_kwargs = {}
    if speaker:
        if Path(speaker).exists():
            tts_kwargs["speaker_wav"] = speaker
        else:
            tts_kwargs["speaker"] = speaker
    audio_path = tmpdir / f"speech_{hash(text)}.wav"
    tts.tts_to_file(text=f"<emotion>{emotion}</emotion> {text}", file_path=str(audio_path), **tts_kwargs)
    return audio_path
