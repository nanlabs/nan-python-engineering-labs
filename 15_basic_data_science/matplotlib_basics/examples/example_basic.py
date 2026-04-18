"""Matplotlib basics example using a non-interactive backend."""

from __future__ import annotations

from io import BytesIO

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt


def main() -> None:
    months = ['Jan', 'Feb', 'Mar', 'Apr']
    sales = [120, 135, 150, 165]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(months, sales, marker='o', color='steelblue')
    ax.set_title('Monthly sales trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Units sold')
    ax.grid(alpha=0.3)

    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=120, bbox_inches='tight')
    print('rendered_bytes:', len(buffer.getvalue()))
    plt.close(fig)


if __name__ == '__main__':
    main()
