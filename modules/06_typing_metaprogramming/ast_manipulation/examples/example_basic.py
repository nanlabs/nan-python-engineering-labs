import ast


class ReplaceName(ast.NodeTransformer):
    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id == "old_value":
            return ast.copy_location(ast.Name(id="new_value", ctx=node.ctx), node)
        return node


def main() -> None:
    """Entry point to demonstrate the implementation."""
    tree = ast.parse("old_value = 10\nprint(old_value)")
    updated = ReplaceName().visit(tree)
    ast.fix_missing_locations(updated)
    print(ast.unparse(updated))


if __name__ == "__main__":
    main()
