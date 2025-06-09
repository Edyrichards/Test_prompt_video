"""Minimal Gradio UI for the video pipeline."""
import gradio as gr
from pathlib import Path
import tempfile

from core.script_generator import generate_script
from core.image_generator import generate_image
from core.audio_generator import generate_audio
from core.video_editor import assemble_video
from core.animation import animate_image


def run_pipeline(prompt, emotion, style):
    segments = generate_script(prompt, emotion)
    images = []
    audios = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for idx, seg in enumerate(segments):
            img = generate_image(seg, emotion, style)
            audio = generate_audio(seg, emotion, None, tmpdir)
            img_path = tmpdir / f"img{idx}.png"
            img.save(img_path)
            video = animate_image(img_path, audio, tmpdir)
            images.append(video)
            audios.append(audio)
        out = tmpdir / "out.mp4"
        assemble_video(images, audios, None, out)
        return out


def app():
    iface = gr.Interface(
        fn=run_pipeline,
        inputs=[gr.Textbox(), gr.Textbox(value="happy"), gr.Dropdown(["anime", "pixar", "realistic"], value="anime")],
        outputs=gr.Video(),
    )
    iface.launch()


if __name__ == "__main__":  # pragma: no cover
    app()

