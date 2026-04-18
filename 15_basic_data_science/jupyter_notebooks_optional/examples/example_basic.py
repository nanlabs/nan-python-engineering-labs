"""Jupyter notebook outline example using plain Python dictionaries."""

from __future__ import annotations

import json


def build_notebook_outline(title: str, sections: list[str]) -> dict[str, object]:
    cells = [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [f'# {title}\n'],
        }
    ]
    for section in sections:
        cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': [f'## {section}\n']})
        cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': ['pass\n']})
    return {'cells': cells, 'metadata': {'kernelspec': {'name': 'python3'}}, 'nbformat': 4, 'nbformat_minor': 5}


def main() -> None:
    outline = build_notebook_outline('Weekly analysis', ['Load data', 'Explore trends', 'Next steps'])
    print(json.dumps({'cells': len(outline['cells']), 'metadata': outline['metadata']}, indent=2))


if __name__ == '__main__':
    main()
