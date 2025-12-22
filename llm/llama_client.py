import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

import os
from groq import Groq

def get_groq_client():
    # 1️⃣ Try normal environment variable (local dev)
    api_key = os.environ.get("GROQ_API_KEY")

    # 2️⃣ Fallback to Streamlit secrets (cloud)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass

    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found")

    return Groq(api_key=api_key)

client = get_groq_client()

# ---------- STREAMING (UI, SSE, Live typing) ----------
def stream_llama(prompt: str, temperature: float = 0.4):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_completion_tokens=800,
        top_p=1,
        stream=True,
    )

    for chunk in completion:
        delta = chunk.choices[0].delta
        if delta and getattr(delta, "content", None):
            yield delta.content


# ---------- NON-STREAMING (Parsing, JSON, Tools) ----------
def call_llama(prompt: str, temperature: float = 0.4) -> str:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_completion_tokens=2000,   # 🔥 WAS TOO LOW
        top_p=1,
        stream=False,
    )
    return completion.choices[0].message.content

