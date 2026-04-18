"""
PyMethods: Rust methods accessible as Python instance methods.
Demonstrates instance and class methods in PyO3.
"""

class Counter:
    """Simple counter class."""
    def __init__(self, initial: int = 0):
        self.value = initial
    
    def increment(self):
        """Increment by 1."""
        self.value += 1
    
    def add(self, amount: int):
        """Add amount to counter."""
        self.value += amount
    
    def get_value(self) -> int:
        """Get current value."""
        return self.value
    
    @staticmethod
    def create_default():
        """Create counter with default value."""
        return Counter(0)

if __name__ == "__main__":
    c = Counter(5)
    c.increment()
    c.add(10)
    print(f"Counter value: {c.get_value()}")
