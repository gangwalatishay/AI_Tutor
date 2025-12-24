from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

from agent.executor import run_video_agent


# ===============================
# Streamlit Page Config
# ===============================

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Video Generator")
st.write(
    "Generate a complete educational video using AI — "
    "script, visuals, narration, and final rendering."
)

# ===============================
# Input
# ===============================

goal = st.text_input(
    "Enter video goal",
    placeholder="Create a 2-minute educational video on Deepfake Detection"
)

# ===============================
# Generate Button
# ===============================

if st.button("🚀 Generate Video"):
    if not goal.strip():
        st.warning("Please enter a video goal.")
        st.stop()

    with st.spinner("⏳ Generating video... this may take a minute"):
        try:
            result = run_video_agent(goal)
        except Exception as e:
            st.error("❌ Video generation failed")
            st.exception(e)
            st.stop()

    # ---------------------------
    # Error handling
    # ---------------------------
    if isinstance(result, dict) and result.get("error"):
        st.error(result["error"])
        st.stop()

    video_path = result.get("video_path")

    if not video_path or not os.path.exists(video_path):
        st.error("❌ Video file was not created.")
        st.stop()

    # ---------------------------
    # Success
    # ---------------------------
    st.success("✅ Video Generated Successfully!")

    st.video(video_path)

    # Optional details
    with st.expander("📄 Generation Details"):
        st.write("**Goal:**", goal)
        st.write("**Scenes Generated:**", len(result.get("scenes", [])))
        st.write("**Video Path:**", video_path)
