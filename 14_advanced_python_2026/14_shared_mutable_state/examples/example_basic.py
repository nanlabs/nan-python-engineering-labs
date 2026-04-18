"""
Shared mutable state with thread safety.
Demonstrates Cell and RefCell patterns.
"""

class SharedCounter:
    """Thread-safe counter (simulated with interior mutability)."""
    def __init__(self, initial: int = 0):
        self._value = initial
    
    def increment(self):
        self._value += 1
    
    def get(self) -> int:
        return self._value

class DataStore:
    """Shared data store with locking."""
    def __init__(self):
        self._data = {}
    
    def set(self, key: str, value):
        self._data[key] = value
    
    def get(self, key: str):
        return self._data.get(key)

if __name__ == "__main__":
    counter = SharedCounter(10)
    counter.increment()
    print(f"Counter: {counter.get()}")
    
    store = DataStore()
    store.set("key1", "value1")
    print(f"Stored: {store.get('key1')}")
