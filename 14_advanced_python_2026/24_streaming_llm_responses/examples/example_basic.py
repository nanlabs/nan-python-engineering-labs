"""
Streaming responses from LLMs.
"""


def stream_response(prompt: str):
    """Simulate streaming LLM response."""
    tokens = ["The", " answer", " is", " streaming"]
    for token in tokens:
        print(token, end="", flush=True)
        yield token
    print()


def accumulate_stream(prompt: str) -> str:
    """Accumulate streamed response."""
    response = ""
    for token in stream_response(prompt):
        response += token
    return response


if __name__ == "__main__":
    full_response = accumulate_stream("What is Python?")
    print(f"\nFull response: {full_response}")
