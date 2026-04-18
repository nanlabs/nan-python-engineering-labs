"""Seaborn visualization example using a bar plot."""

from __future__ import annotations

from io import BytesIO

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    sns.set_theme(style='whitegrid')
    df = pd.DataFrame(
        [
            {'segment': 'enterprise', 'avg_revenue': 220.0},
            {'segment': 'startup', 'avg_revenue': 150.0},
            {'segment': 'mid-market', 'avg_revenue': 180.0},
        ]
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x='segment', y='avg_revenue', palette='crest', ax=ax)
    ax.set_title('Average revenue by segment')
    ax.set_xlabel('Segment')
    ax.set_ylabel('Average revenue')

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=120, bbox_inches='tight')
    print('rendered_bytes:', len(buffer.getvalue()))
    plt.close(fig)


if __name__ == '__main__':
    main()
