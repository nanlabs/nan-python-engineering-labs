"""Inspect Python code with the ast module."""

import ast


class BinOpCounter(ast.NodeVisitor):
    def __init__(self) -> None:
        self.count = 0

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self.count += 1
        self.generic_visit(node)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    code = "result = (a + b) * (c - d) / 2"
    tree = ast.parse(code)
    counter = BinOpCounter()
    counter.visit(tree)
    print(counter.count)


if __name__ == "__main__":
    main()
