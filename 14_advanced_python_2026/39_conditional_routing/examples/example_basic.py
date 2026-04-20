"""
Conditional routing in LangGraph.
"""


def route_based_on_condition(value: int) -> str:
    """Route based on condition."""
    if value < 10:
        return "low_priority"
    elif value < 50:
        return "medium_priority"
    else:
        return "high_priority"


def create_conditional_router() -> dict:
    """Create routing configuration."""
    return {
        "type": "conditional",
        "conditions": [
            {"threshold": 10, "path": "low"},
            {"threshold": 50, "path": "medium"},
            {"threshold": 100, "path": "high"},
        ],
    }


if __name__ == "__main__":
    print(route_based_on_condition(5))
    print(route_based_on_condition(25))
    print(route_based_on_condition(75))
