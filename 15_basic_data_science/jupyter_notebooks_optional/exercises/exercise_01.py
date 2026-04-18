"""Exercise: Jupyter Notebooks (Optional).

Goal: Build a notebook outline that separates markdown narrative from executable code cells.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Keep the output compatible with the notebook JSON schema.
3. Run tests with: pytest tests/
4. Favor clarity over adding many optional metadata fields.
"""

from __future__ import annotations


def build_notebook_outline(title: str, sections: list[str]) -> dict[str, object]:
    """Return a minimal notebook dictionary with markdown and code cells."""
    raise NotImplementedError('Implement build_notebook_outline in my_solution/exercise_01.py')


def count_code_cells(notebook: dict[str, object]) -> int:
    """Return the number of code cells in the notebook structure."""
    raise NotImplementedError('Implement count_code_cells in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to inspect the expected notebook shape."""
    print('Copy this file into my_solution/ and build a small notebook outline.')


if __name__ == '__main__':
    main()
