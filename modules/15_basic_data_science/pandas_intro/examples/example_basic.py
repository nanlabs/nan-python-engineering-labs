"""Pandas introduction example with revenue calculation."""

from __future__ import annotations

import pandas as pd


def main() -> None:
    """Entry point to demonstrate the implementation."""
    records = [
        {"month": "2026-01", "region": "north", "units": 120, "unit_price": 5.5},
        {"month": "2026-01", "region": "south", "units": 90, "unit_price": 6.0},
        {"month": "2026-02", "region": "north", "units": 140, "unit_price": 5.5},
    ]
    df = pd.DataFrame(records)
    df["revenue"] = df["units"] * df["unit_price"]
    revenue_by_month = df.groupby("month", as_index=False)["revenue"].sum()

    print(df[["month", "region", "revenue"]].to_dict(orient="records"))
    print(revenue_by_month.to_dict(orient="records"))


if __name__ == "__main__":
    main()
