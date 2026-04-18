"""
Memory systems for LLMs.
"""

class ConversationMemory:
    """Track conversation history."""
    def __init__(self, max_messages: int = 10):
        self.messages = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def get_history(self) -> list:
        return self.messages

if __name__ == "__main__":
    memory = ConversationMemory()
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there")
    print(f"History: {memory.get_history()}")
