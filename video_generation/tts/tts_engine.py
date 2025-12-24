import os
import platform
import subprocess
import tempfile


def generate_audio(text: str, output_path: str):
    """
    Cross-platform Text-to-Speech engine.

    - macOS → uses native `say` command (offline, high quality)
    - Linux / Streamlit Cloud → uses gTTS (cloud-safe)

    Output format: WAV (MoviePy compatible)
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    system = platform.system()

    # =============================
    # macOS (local development)
    # =============================
    if system == "Darwin":
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
            tmp_aiff = tmp.name

        # Generate speech using macOS "say"
        subprocess.run(
            ["say", "-o", tmp_aiff, text],
            check=True
        )

        # Convert AIFF → WAV using ffmpeg
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

    # =============================
    # Linux / Streamlit Cloud
    # =============================
    else:
        # Lazy import to avoid startup crash
        from gtts import gTTS

        tts = gTTS(text=text, lang="en")
        tts.save(output_path)

    print(f"[TTS] Audio created → {output_path}")
