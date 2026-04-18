"""
LangChain chains advanced patterns.
"""

class SimpleChain:
    """Simple chain implementation."""
    def __init__(self, name: str):
        self.name = name
        self.steps = []
    
    def add_step(self, step: str):
        self.steps.append(step)
    
    def execute(self, input_data: str) -> str:
        result = input_data
        for step in self.steps:
            result = f"{result} -> {step}"
        return result

if __name__ == "__main__":
    chain = SimpleChain("query")
    chain.add_step("retrieve_docs")
    chain.add_step("rank_results")
    chain.add_step("format_answer")
    
    output = chain.execute("What is Python?")
    print(f"Chain output: {output}")
