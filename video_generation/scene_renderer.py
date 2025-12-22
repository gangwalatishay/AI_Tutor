# from moviepy.editor import ImageClip, AudioFileClip
# from PIL import Image

# # 🔧 Pillow 10+ compatibility patch
# if not hasattr(Image, "ANTIALIAS"):
#     Image.ANTIALIAS = Image.Resampling.LANCZOS


# def render_scene(scene, resolution=(1280, 720)):
#     """
#     Renders a single scene using an image + narration audio.
#     """

#     image_path = scene["image_path"]
#     audio_path = scene["audio_path"]

#     audio_clip = AudioFileClip(audio_path)

#     image_clip = (
#         ImageClip(image_path)
#         .resize(resolution)
#         .set_duration(audio_clip.duration)
#         .set_audio(audio_clip)
#     )

#     return image_clip
# from video_generation.charts.chart_renderer import render_chart
# from video_generation.infographics.infographics_renderer import render_infographic
# from moviepy.editor import ImageClip, AudioFileClip


# def render_scene(scene):
#     audio = AudioFileClip(scene["audio_path"])

#     if scene["scene_type"] == "chart":
#         image_path = f"video_generation/output/chart_{scene['scene_number']}.png"
#         render_chart(scene, image_path)

#     elif scene["scene_type"] == "infographic":
#         image_path = f"video_generation/output/info_{scene['scene_number']}.png"
#         render_infographic(scene, image_path)

#     else:
#         image_path = scene["image_path"]

#     clip = ImageClip(image_path).set_duration(audio.duration)
#     clip = clip.set_audio(audio)

#     return clip


# from moviepy.editor import ImageClip, AudioFileClip
# from .infographics import render_infographic
# from video_generation.image_generation.image_engine import generate_image
# import os


# def render_scene(scene, resolution=(1920, 1080)):
#     """
#     Renders one scene safely.
#     Supports:
#     - image
#     - infographic
#     - chart (future)
#     """

#     # ✅ SAFE defaults
#     scene_type = scene.get("scene_type", "image")
#     audio_path = scene.get("audio_path")

#     output_image = f"video_generation/output/scene_{scene['scene_number']}.png"

#     # ---------------------------
#     # VISUAL SELECTION
#     # ---------------------------
#     if scene_type == "infographic":
#         image_path = render_infographic(scene, output_image)

#     elif scene_type == "chart":
#         # Placeholder for charts (no crash)
#         image_path = generate_image(
#             scene.get("visual_description", "Chart"),
#             output_image
#         )

#     else:
#         # Default = image
#         image_path = generate_image(
#             scene.get("visual_description", ""),
#             output_image
#         )

#     # ---------------------------
#     # AUDIO
#     # ---------------------------
#     audio_clip = AudioFileClip(audio_path)
#     duration = audio_clip.duration

#     video_clip = (
#         ImageClip(image_path)
#         .resize(resolution)
#         .set_duration(duration)
#         .set_audio(audio_clip)
#     )

#     return video_clip

import os
import numpy as np
from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image

from video_generation.image_generation.image_engine import generate_image
from video_generation.infographics.infographic_renderer import render_infographic


def render_scene(scene, resolution=(1920, 1080)):
    """
    Renders a single scene safely.

    Supported scene types:
    - image (default)
    - infographic
    - chart (fallback to image for now)
    """

    scene_number = scene["scene_number"]
    scene_type = scene.get("scene_type", "image")
    audio_path = scene["audio_path"]

    output_dir = "video_generation/output"
    os.makedirs(output_dir, exist_ok=True)

    image_path = os.path.join(output_dir, f"scene_{scene_number}.png")

    # =============================
    # GENERATE VISUAL
    # =============================
    if scene_type == "infographic":
        image_path = render_infographic(scene, image_path)

    elif scene_type == "chart":
        # Temporary fallback → image until animated charts added
        image_path = generate_image(
            scene.get("visual_description", "Chart visualization"),
            image_path
        )

    else:
        # Default image generation
        image_path = generate_image(
            scene.get("visual_description", ""),
            image_path
        )

    # =============================
    # LOAD AUDIO
    # =============================
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # =============================
    # SAFE IMAGE RESIZE (Pillow ≥10)
    # =============================
    img = Image.open(image_path).convert("RGB")
    img = img.resize(resolution, Image.Resampling.LANCZOS)
    img_array = np.array(img)

    video_clip = (
        ImageClip(img_array)
        .set_duration(duration)
        .set_audio(audio_clip)
    )

    return video_clip
