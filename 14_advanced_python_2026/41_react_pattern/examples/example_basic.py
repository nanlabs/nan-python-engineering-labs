"""
ReAct pattern: Reasoning + Acting.
"""

def act_step(action: str, input_data: str) -> str:
    """Perform action."""
    return f"Result of {action} on {input_data}"

def think_step(observation: str) -> str:
    """Reasoning step."""
    return f"Thinking about: {observation}"

def react_loop(initial_task: str) -> list:
    """ReAct loop iteration."""
    steps = [
        think_step("Initial problem analysis"),
        act_step("search", initial_task),
        think_step("Refine approach"),
        act_step("process_results", "search_results"),
    ]
    return steps

if __name__ == "__main__":
    steps = react_loop("What is AI?")
    for step in steps:
        print(f"  {step}")
