"""Video editing and assembly module."""
import logging
from pathlib import Path
from typing import List, Union
import tempfile

from PIL import Image
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    VideoFileClip,
    concatenate_videoclips,
    CompositeAudioClip,
    vfx,
)


def _image_to_clip(img: Union[Image.Image, Path]) -> ImageClip:
    if isinstance(img, Path):
        if img.suffix == ".mp4":
            return VideoFileClip(str(img)).subclip(0, 10)
        return ImageClip(str(img)).set_duration(10)
    else:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as fp:
            img.save(fp.name)
            return ImageClip(fp.name).set_duration(10)


def assemble_video(
    clips: List[Union[Image.Image, Path]],
    audios: List[Path],
    music: Path,
    out_path: Path,
) -> None:
    """Combine clips, audio and music into a final mp4."""
    logging.info("Assembling final video")
    video_clips = []
    for img, audio in zip(clips, audios):
        clip = _image_to_clip(img)
        clip = clip.fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5)
        clip = clip.fx(vfx.zoom_in, 1.05)
        clip = clip.set_audio(AudioFileClip(str(audio)).set_duration(10))
        video_clips.append(clip)
    final = concatenate_videoclips(video_clips, method="compose")
    if music and music.exists():
        bg = AudioFileClip(str(music)).volumex(0.3).audio_loop(duration=final.duration)
        final = final.set_audio(CompositeAudioClip([final.audio, bg]))
    final.write_videofile(str(out_path), fps=24)
