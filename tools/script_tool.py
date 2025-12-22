from llm.llama_client import call_llama

def generate_script(goal: str) -> str:
    """
    Generates a narration script for the video using base LLaMA.
    """

    with open("prompts/script.txt", "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{{TOPIC}}", goal)

    script = call_llama(
        prompt=prompt,
        temperature=0.4  # slightly creative, but controlled
    )

    return script.strip()
