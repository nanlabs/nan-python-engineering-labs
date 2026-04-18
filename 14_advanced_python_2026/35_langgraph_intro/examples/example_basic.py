"""
LangGraph fundamentals.
"""

class Graph:
    """Simple graph structure."""
    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def add_node(self, name: str, function):
        self.nodes[name] = function
    
    def add_edge(self, from_node: str, to_node: str):
        self.edges.append((from_node, to_node))
    
    def get_topology(self) -> dict:
        return {"nodes": len(self.nodes), "edges": len(self.edges)}

if __name__ == "__main__":
    graph = Graph()
    graph.add_node("start", lambda x: x)
    graph.add_node("process", lambda x: x * 2)
    graph.add_edge("start", "process")
    print(f"Graph: {graph.get_topology()}")
