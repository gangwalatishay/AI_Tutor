import os

LLAMA_API_KEY = os.getenv("GROQ_API_KEY")

if not LLAMA_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in environment variables")
