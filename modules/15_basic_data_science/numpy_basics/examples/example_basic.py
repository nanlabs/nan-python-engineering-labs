"""NumPy basics example with vectorized operations."""

import numpy as np


def main() -> None:
    """Entry point to demonstrate the implementation."""
    sales = np.array([120.0, 135.0, 150.0, 165.0])
    operating_cost = np.array([48.0, 51.0, 55.0, 58.0])
    margin = sales - operating_cost
    growth_pct = np.diff(sales) / sales[:-1]
    z_scores = (sales - sales.mean()) / sales.std()

    print("margin:", margin.round(2).tolist())
    print("growth_pct:", (growth_pct * 100).round(2).tolist())
    print("z_scores:", z_scores.round(2).tolist())


if __name__ == "__main__":
    main()
