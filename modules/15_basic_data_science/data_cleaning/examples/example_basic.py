"""Data cleaning example with standardization and missing values."""

from __future__ import annotations

import pandas as pd


def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [column.strip().lower().replace(" ", "_") for column in cleaned.columns]
    cleaned["customer_name"] = cleaned["customer_name"].str.strip().str.title()
    cleaned["revenue"] = cleaned["revenue"].fillna(cleaned["revenue"].median())
    cleaned = cleaned.drop_duplicates(subset=["customer_id"])
    return cleaned.sort_values("customer_id").reset_index(drop=True)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    raw = pd.DataFrame(
        [
            {"Customer ID": 2, "Customer Name": "  ana ", "Revenue": 1200.0},
            {"Customer ID": 1, "Customer Name": "luis", "Revenue": None},
            {"Customer ID": 2, "Customer Name": "ANA", "Revenue": 1200.0},
        ]
    )
    cleaned = clean_customer_data(raw)
    print(cleaned.to_dict(orient="records"))


if __name__ == "__main__":
    main()
