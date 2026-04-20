"""
Multi-agent collaboration.
"""


class Agent:
    """Individual agent."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def get_info(self) -> dict:
        return {"name": self.name, "role": self.role}


class MultiAgentSystem:
    """Coordinate multiple agents."""

    def __init__(self):
        self.agents = []

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def get_agents_info(self) -> list:
        return [a.get_info() for a in self.agents]


if __name__ == "__main__":
    system = MultiAgentSystem()
    system.add_agent(Agent("Alice", "analyst"))
    system.add_agent(Agent("Bob", "coder"))

    info = system.get_agents_info()
    print(f"Agents: {info}")
