from llm.llama_client import call_llama
from prompts.loader import load_prompt

def generate_script(goal: str) -> str:
    prompt = load_prompt("script.txt", goal=goal)
    return call_llama(prompt, temperature=0.3)

