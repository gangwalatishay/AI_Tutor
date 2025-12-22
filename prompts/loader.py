from pathlib import Path

PROMPT_DIR = Path(__file__).parent

def load_prompt(name: str, **kwargs) -> str:
    text = (PROMPT_DIR / name).read_text()
    for k, v in kwargs.items():
        text = text.replace(f"{{{{{k}}}}}", v)
    return text
