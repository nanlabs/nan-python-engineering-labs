"""Exercise: NumPy Basics.

Goal: Implement reusable NumPy helpers for normalization and smoothing.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Implement both functions using vectorized NumPy operations.
3. Run tests with: pytest tests/
4. Keep edge cases explicit and documented.
"""

from __future__ import annotations

import numpy as np


def normalize_scores(values: np.ndarray) -> np.ndarray:
    """Return the z-score normalized version of a one-dimensional array."""
    raise NotImplementedError('Implement normalize_scores in my_solution/exercise_01.py')


def moving_average(values: np.ndarray, window: int) -> np.ndarray:
    """Return the moving average for the provided window size."""
    raise NotImplementedError('Implement moving_average in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to try local experiments in your own copy."""
    sample = np.array([10.0, 12.0, 14.0, 16.0])
    print('Copy this file into my_solution/ and experiment with:', sample.tolist())


if __name__ == '__main__':
    main()
