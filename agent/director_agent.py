import json
from llm.llama_client import call_llama


def director_agent(script: str):
    prompt = f"""
You are a professional video director.

Convert the following narration script into a STRICT JSON array of scenes.

RULES (VERY IMPORTANT):
- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text
- Return an array of objects
- Each object MUST have:
  - scene_number (int)
  - time_range (string)
  - visual_description (string)
  - narration_text (string)

SCRIPT:
{script}
"""

    response = call_llama(prompt, temperature=0.2)

    try:
        scenes = json.loads(response)
        return scenes
    except Exception as e:
        print("❌ Director raw output:\n", response)
        raise ValueError("Director agent produced invalid JSON")
