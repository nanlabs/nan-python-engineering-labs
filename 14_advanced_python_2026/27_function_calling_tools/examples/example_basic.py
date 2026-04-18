"""
Function calling and tool use in LLMs.
"""

def define_tool(name: str, description: str, params: dict) -> dict:
    """Define a tool for LLM."""
    return {
        "name": name,
        "description": description,
        "parameters": params,
    }

def create_tools_list() -> list:
    """Create list of available tools."""
    return [
        define_tool("calculate", "Calculate math expression", {"expr": "string"}),
        define_tool("search", "Search online", {"query": "string"}),
    ]

if __name__ == "__main__":
    tools = create_tools_list()
    print(f"Available tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
