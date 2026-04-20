"""
Nodes and edges in LangGraph.
"""


class Node:
    """Graph node."""

    def __init__(self, name: str, processor):
        self.name = name
        self.processor = processor

    def execute(self, input_data):
        return self.processor(input_data)


class Edge:
    """Graph edge."""

    def __init__(self, from_node: str, to_node: str, condition=None):
        self.from_node = from_node
        self.to_node = to_node
        self.condition = condition


if __name__ == "__main__":
    node = Node("process", lambda x: x * 2)
    edge = Edge("start", "process")

    print(f"Node: {node.name}")
    print(f"Edge: {edge.from_node} -> {edge.to_node}")
