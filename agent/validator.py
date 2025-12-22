import json

REQUIRED_SCENE_KEYS = {
    "scene_number",
    "time_range",
    "visual_description",
    "narration_text",
}

def validate_scenes(raw_output: str):
    """
    Validates Director Agent output.
    Returns (is_valid: bool, data_or_error)
    """

    # 1. Must be valid JSON
    try:
        scenes = json.loads(raw_output)
    except Exception as e:
        return False, f"Invalid JSON: {str(e)}"

    # 2. Must be a list
    if not isinstance(scenes, list):
        return False, "Scenes must be a JSON array"

    # 3. Must not be empty
    if len(scenes) == 0:
        return False, "Scenes array is empty"

    # 4. Validate each scene
    for idx, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            return False, f"Scene {idx} is not an object"

        missing = REQUIRED_SCENE_KEYS - scene.keys()
        if missing:
            return False, f"Scene {idx} missing keys: {missing}"

        # 5. Basic sanity checks
        if not isinstance(scene["scene_number"], int):
            return False, f"Scene {idx} scene_number must be int"

        if not isinstance(scene["time_range"], str):
            return False, f"Scene {idx} time_range must be string"

        if not scene["narration_text"].strip():
            return False, f"Scene {idx} narration_text is empty"

    return True, scenes
