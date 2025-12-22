from agent.validators import validate_script, validate_scenes


def qa_agent(script: str, scenes: list) -> bool:
    if not validate_script(script):
        return False

    if not validate_scenes(scenes):
        return False

    return True
