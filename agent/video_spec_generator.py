def time_to_seconds(t: str) -> int:
    """
    Converts 'M:SS' into seconds.
    """
    minutes, seconds = t.split(":")
    return int(minutes) * 60 + int(seconds)


def generate_video_spec(scenes: list, style: str = "educational") -> dict:
    video_scenes = []

    for scene in scenes:
        start_str, end_str = scene["time_range"].split("-")

        start = time_to_seconds(start_str.strip())
        end = time_to_seconds(end_str.strip())

        video_scenes.append({
            "start": start,
            "end": end,
            "duration": end - start,
            "visual_prompt": scene["visual_description"],
            "voiceover": scene["narration_text"],
            "camera": "static shot, slow zoom",
            "effects": "clean transitions, light motion graphics"
        })

    return {
        "video_spec": {
            "duration": video_scenes[-1]["end"],
            "aspect_ratio": "16:9",
            "fps": 30,
            "style": style,
            "scenes": video_scenes
        }
    }
