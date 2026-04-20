"""Polars introduction example with grouped summaries."""

from __future__ import annotations

import polars as pl


def main() -> None:
    """Entry point to demonstrate the implementation."""
    frame = pl.DataFrame(
        {
            "warehouse": ["east", "west", "east", "north"],
            "items": [120, 90, 80, 60],
            "shipping_cost": [30.0, 22.0, 20.0, 18.0],
        }
    )
    summary = (
        frame.group_by("warehouse")
        .agg(
            pl.col("items").sum().alias("total_items"),
            pl.col("shipping_cost").mean().round(2).alias("avg_shipping_cost"),
        )
        .sort("total_items", descending=True)
    )
    print(summary.to_dicts())


if __name__ == "__main__":
    main()
