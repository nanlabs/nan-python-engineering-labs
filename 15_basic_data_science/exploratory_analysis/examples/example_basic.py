"""Exploratory analysis example with a compact report."""

from __future__ import annotations

import pandas as pd


def compute_eda_report(df: pd.DataFrame) -> dict[str, object]:
    numeric_summary = df[['revenue', 'units']].agg(['mean', 'median', 'max']).round(2)
    top_region = df['region'].value_counts().idxmax()
    return {
        'rows': len(df),
        'numeric_summary': numeric_summary.to_dict(),
        'top_region': top_region,
    }


def main() -> None:
    df = pd.DataFrame(
        [
            {'region': 'north', 'revenue': 1200.0, 'units': 12},
            {'region': 'south', 'revenue': 950.0, 'units': 10},
            {'region': 'north', 'revenue': 1400.0, 'units': 14},
        ]
    )
    print(compute_eda_report(df))


if __name__ == '__main__':
    main()
