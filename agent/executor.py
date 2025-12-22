# from agent.planner import plan_video_tasks
# from agent.writer_agent import writer_agent
# from agent.director_agent import director_agent
# from agent.qa_agent import qa_agent

# from video_generation.tts import generate_audio
# from video_generation.image_generation import generate_image
# from video_generation.build_video import build_video


# def run_video_agent(goal: str):
#     # 1. Planner
#     plan = plan_video_tasks(goal)

#     # 2. Script
#     script = writer_agent(goal)

#     # 3. Scenes
#     scenes = director_agent(script)

#     # 4. QA
#     if not qa_agent(script, scenes):
#         return {"error": "QA rejected output"}

#     # 5. Generate media
#     for i, scene in enumerate(scenes):
#         audio_path = f"video_generation/output/audio_{i}.wav"
#         image_path = f"video_generation/output/image_{i}.png"

#         generate_audio(scene["narration_text"], audio_path)
#         generate_image(scene["visual_description"], image_path)

#         scene["audio_path"] = audio_path
#         scene["image_path"] = image_path

#     # 6. Build final video
#     video_path = build_video(scenes)

#     return {
#         "plan": plan,
#         "script": script,
#         "scenes": scenes,
#         "video_path": video_path

#     }
import os
from typing import List, Dict

from agent.planner import plan_video_tasks
from agent.writer_agent import writer_agent
from agent.director_agent import director_agent
from agent.qa_agent import qa_agent

from video_generation.tts.tts_engine import generate_audio
from video_generation.image_generation.image_engine import generate_image
from video_generation.build_video import build_video


# ===============================
# Helpers
# ===============================

REQUIRED_SCENE_KEYS = {
    "scene_number",
    "time_range",
    "visual_description",
    "narration_text",
}


def validate_scenes(scenes: List[Dict]) -> List[Dict]:
    """
    Hard validation to avoid runtime crashes.
    """
    if not isinstance(scenes, list) or len(scenes) == 0:
        raise ValueError("Director agent must return a non-empty list of scenes")

    for i, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            raise ValueError(f"Scene {i} is not a dictionary")

        missing = REQUIRED_SCENE_KEYS - scene.keys()
        if missing:
            raise ValueError(f"Scene {i} missing keys: {missing}")

    return scenes


# ===============================
# MAIN PIPELINE
# ===============================

def run_video_agent(goal: str) -> dict:
    """
    Full non-streaming pipeline.
    Safe, validated, Streamlit-compatible.
    """

    # ---------------------------
    # 1️⃣ Planner
    # ---------------------------
    plan = plan_video_tasks(goal)

    # ---------------------------
    # 2️⃣ Writer
    # ---------------------------
    script = writer_agent(goal)

    # ---------------------------
    # 3️⃣ Director
    # ---------------------------
    raw_scenes = director_agent(script)
    scenes = validate_scenes(raw_scenes)

    # ---------------------------
    # 4️⃣ QA Agent
    # ---------------------------
    if not qa_agent(script, scenes):
        return {"error": "QA agent rejected output"}

    # ---------------------------
    # 5️⃣ Media Generation
    # ---------------------------
    os.makedirs("video_generation/output", exist_ok=True)

    for i, scene in enumerate(scenes):
        audio_path = f"video_generation/output/audio_{i}.wav"
        image_path = f"video_generation/output/image_{i}.png"

        # 🔊 Audio
        generate_audio(scene["narration_text"], audio_path)

        # 🖼️ Image / Visual
        generate_image(scene["visual_description"], image_path)

        # Attach paths
        scene["audio_path"] = audio_path
        scene["image_path"] = image_path

        # Optional defaults (future-proofing)
        scene.setdefault("scene_type", "image")

    # ---------------------------
    # 6️⃣ Video Rendering
    # ---------------------------
    video_path = build_video(scenes)

    # ---------------------------
    # 7️⃣ Final Output
    # ---------------------------
    return {
        "plan": plan,
        "script": script,
        "scenes": scenes,
        "video_path": video_path,
    }
