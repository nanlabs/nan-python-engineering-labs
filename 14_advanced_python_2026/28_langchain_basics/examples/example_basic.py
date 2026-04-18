"""
LangChain fundamentals.
"""

def create_chain_simple(prompt: str) -> str:
    """Simple chain simulation."""
    steps = [
        "1. Parse prompt",
        "2. Call LLM",
        "3. Format response",
    ]
    return f"Chain for '{prompt}': {steps}"

def chain_composition(input_text: str) -> dict:
    """Compose multiple chains."""
    return {
        "input": input_text,
        "chain1_output": "processed_1",
        "chain2_output": "processed_2",
        "final_output": "final_result",
    }

if __name__ == "__main__":
    result = create_chain_simple("What is AI?")
    print(result)
    
    composed = chain_composition("test")
    print(f"Composition: {composed}")
