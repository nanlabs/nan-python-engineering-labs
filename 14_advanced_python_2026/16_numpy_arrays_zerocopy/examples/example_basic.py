"""
NumPy arrays with zero-copy semantics.
Direct access to NumPy buffer from Rust.
"""

import numpy as np

def process_numpy_array(arr: np.ndarray) -> np.ndarray:
    """Process NumPy array with zero-copy (simulated)."""
    return arr * 2

def array_statistics(arr: np.ndarray) -> dict:
    """Compute statistics on NumPy array."""
    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "sum": float(np.sum(arr)),
    }

if __name__ == "__main__":
    arr = np.array([1, 2, 3, 4, 5])
    print("Original:", arr)
    print("Processed:", process_numpy_array(arr))
    print("Stats:", array_statistics(arr))
