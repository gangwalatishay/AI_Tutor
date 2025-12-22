def seconds_to_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def generate_srt(scenes, output_path):
    current_time = 0.0
    lines = []

    for idx, scene in enumerate(scenes, start=1):
        text = scene["narration_text"]
        duration = scene.get("duration", 4.0)

        start = seconds_to_srt_time(current_time)
        end = seconds_to_srt_time(current_time + duration)

        lines.append(f"{idx}")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")

        current_time += duration

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("✅ Subtitles saved:", output_path)
