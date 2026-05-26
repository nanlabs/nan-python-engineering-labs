"""
State management in LangGraph.
"""


class GraphState:
    """Manage graph state."""

    def __init__(self):
        self.state = {}
        self.history = []

    def update(self, key: str, value):
        self.state[key] = value
        self.history.append((key, value))

    def get(self, key: str):
        return self.state.get(key)

    def get_history(self) -> list:
        return self.history


if __name__ == "__main__":
    state = GraphState()
    state.update("counter", 0)
    state.update("counter", 1)
    print(f"Current state: {state.get('counter')}")
    print(f"History: {state.get_history()}")
