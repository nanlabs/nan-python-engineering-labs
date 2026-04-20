"""Pandas performance example comparing apply and vectorization."""

from __future__ import annotations

from time import perf_counter

import pandas as pd


def apply_discount_vectorized(df: pd.DataFrame, threshold: float, rate: float) -> pd.Series:
    return df["revenue"].where(df["revenue"] < threshold, df["revenue"] * (1 - rate))


def main() -> None:
    """Entry point to demonstrate the implementation."""
    df = pd.DataFrame({"revenue": [100.0, 200.0, 150.0, 80.0] * 1000})

    start = perf_counter()
    vectorized = apply_discount_vectorized(df, threshold=120.0, rate=0.1)
    vectorized_ms = (perf_counter() - start) * 1000

    start = perf_counter()
    apply_based = df["revenue"].apply(lambda value: value if value < 120.0 else value * 0.9)
    apply_ms = (perf_counter() - start) * 1000

    print(
        {
            "vectorized_ms": round(vectorized_ms, 3),
            "apply_ms": round(apply_ms, 3),
            "same_values": vectorized.equals(apply_based),
        }
    )


if __name__ == "__main__":
    main()
