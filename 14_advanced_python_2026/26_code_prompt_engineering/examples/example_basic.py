"""
Prompt engineering techniques for code generation.
"""

def create_system_prompt() -> str:
    """Create effective system prompt."""
    return "You are expert Python programmer. Generate clean, efficient code."

def create_user_prompt(task: str) -> str:
    """Create user prompt for task."""
    return f"Task: {task}\nProvide Python code solution."

def combine_prompts(task: str) -> dict:
    """Combine system and user prompts."""
    return {
        "system": create_system_prompt(),
        "user": create_user_prompt(task),
    }

if __name__ == "__main__":
    prompts = combine_prompts("Sort a list")
    print(f"Prompts: {prompts}")
