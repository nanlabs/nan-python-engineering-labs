"""
Python callbacks invoked from Rust code.
Demonstrates passing Python functions to Rust.
"""

def call_callback(callback, data):
    """Invoke a Python callback from Rust context."""
    return callback(data)

def process_with_callback(items: list, callback) -> list:
    """Process list items with callback."""
    return [callback(x) for x in items]

if __name__ == "__main__":
    def double(x):
        return x * 2
    
    result = call_callback(double, 5)
    print(f"Callback result: {result}")
    
    items = [1, 2, 3]
    processed = process_with_callback(items, double)
    print(f"Processed: {processed}")
