"""
Implementing Python classes with Rust.
Shows how to create class-like objects from Rust code.
"""

class DataProcessor:
    """Mock Rust-based data processor."""
    def __init__(self, name: str):
        self.name = name
        self.data = []
    
    def add_value(self, value: int):
        """Add value to internal buffer."""
        self.data.append(value)
    
    def get_stats(self) -> dict:
        """Compute statistics on stored data."""
        if not self.data:
            return {"count": 0, "sum": 0, "avg": 0}
        return {
            "count": len(self.data),
            "sum": sum(self.data),
            "avg": sum(self.data) / len(self.data),
        }

if __name__ == "__main__":
    proc = DataProcessor("test")
    proc.add_value(10)
    proc.add_value(20)
    proc.add_value(30)
    print(proc.get_stats())
