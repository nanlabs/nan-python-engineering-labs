"""
LLM cost tracking and optimization.
"""

def calculate_token_cost(tokens: int, model: str) -> float:
    """Calculate cost based on tokens."""
    rates = {
        "gpt-3.5": 0.0005,
        "gpt-4": 0.03,
    }
    rate = rates.get(model, 0.001)
    return tokens * rate / 1000

def track_request(model: str, input_tokens: int, output_tokens: int) -> dict:
    """Track single request cost."""
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": calculate_token_cost(input_tokens + output_tokens, model),
    }

if __name__ == "__main__":
    request = track_request("gpt-3.5", 100, 50)
    print(f"Request: {request}")
    print(f"Cost: ${request['cost']:.6f}")
