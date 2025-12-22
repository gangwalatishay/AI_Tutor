import os
import subprocess
import tempfile


def generate_audio(text: str, output_path: str):
    """
    Generate WAV audio using macOS 'say' command (stable, offline).
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Use temp AIFF (say outputs AIFF reliably)
    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
        tmp_aiff = tmp.name

    # Generate speech
    subprocess.run(
        ["say", "-o", tmp_aiff, text],
        check=True
    )

    # Convert AIFF → WAV (MoviePy-friendly)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", tmp_aiff,
            "-ac", "1",
            "-ar", "22050",
            output_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    os.remove(tmp_aiff)

    print(f"[TTS] Audio created → {output_path}")
