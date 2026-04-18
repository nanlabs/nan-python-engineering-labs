"""Pandas operations example with merge and aggregation."""

from __future__ import annotations

import pandas as pd


def main() -> None:
    orders = pd.DataFrame(
        [
            {'customer_id': 1, 'amount': 120.0},
            {'customer_id': 2, 'amount': 80.0},
            {'customer_id': 1, 'amount': 60.0},
        ]
    )
    customers = pd.DataFrame(
        [
            {'customer_id': 1, 'segment': 'enterprise'},
            {'customer_id': 2, 'segment': 'startup'},
        ]
    )
    summary = (
        orders.merge(customers, on='customer_id', how='left')
        .groupby('segment', as_index=False)
        .agg(total_revenue=('amount', 'sum'), average_order_value=('amount', 'mean'))
    )
    print(summary.round(2).to_dict(orient='records'))


if __name__ == '__main__':
    main()
