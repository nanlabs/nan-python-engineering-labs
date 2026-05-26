"""
Comparing LangChain chains vs LangGraph graphs.
"""


def explain_chains() -> dict:
    """Chains: Sequential, linear flow."""
    return {
        "type": "Chain",
        "flow": "Linear",
        "branching": False,
        "use_case": "Simple sequential processing",
    }


def explain_graphs() -> dict:
    """Graphs: Complex, non-linear flow."""
    return {
        "type": "Graph",
        "flow": "Non-linear",
        "branching": True,
        "use_case": "Complex workflows with decisions",
    }


if __name__ == "__main__":
    chain_info = explain_chains()
    graph_info = explain_graphs()
    print(f"Chains: {chain_info}")
    print(f"Graphs: {graph_info}")
