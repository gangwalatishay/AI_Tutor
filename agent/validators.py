def validate_script(text: str) -> bool:
    if not isinstance(text, str):
        return False

    word_count = len(text.split())
    return 160 <= word_count <= 240


def validate_scenes(scenes) -> bool:
    if not isinstance(scenes, list):
        return False

    required_keys = {
        "scene_number",
        "time_range",
        "visual_description",
        "narration_text",
    }

    for scene in scenes:
        if not isinstance(scene, dict):
            return False
        if not required_keys.issubset(scene.keys()):
            return False

    return True
