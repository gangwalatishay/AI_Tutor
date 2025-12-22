
from llm.llama_client import call_llama

PLANNER_TEMPERATURE = 0.3

def plan_video_tasks(goal: str) -> list:
    with open("prompts/planner.txt", "r") as f:
        system_prompt = f.read()

    prompt = f"""
{system_prompt}

Video Goal:
{goal}
"""

    response = call_llama(prompt, temperature=PLANNER_TEMPERATURE)

    # Parse tasks safely
    tasks = [
        line.strip()
        for line in response.split("\n")
        if line.strip()
    ]

    return tasks
