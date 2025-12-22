import os
from moviepy.editor import concatenate_videoclips
from video_generation.scene_renderer import render_scene


OUTPUT_DIR = "video_generation/output"
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final_video.mp4")


def build_video(scenes):
    """
    Build full video from rendered scenes.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    clips = []

    for scene in scenes:
        clip = render_scene(scene)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")

    final.write_videofile(
        FINAL_VIDEO,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    final.close()
    for c in clips:
        c.close()

    return FINAL_VIDEO
