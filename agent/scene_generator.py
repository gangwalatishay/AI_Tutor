from llm.llama_client import call_llama
from prompts.loader import load_prompt
import json

def generate_scenes(script: str):
    prompt = load_prompt("scenes.txt", script=script)
    response = call_llama(prompt, temperature=0.2)

    try:
        return json.loads(response)
    except Exception:
        return {
            "error": "Invalid scene JSON",
            "raw_output": response
        }
