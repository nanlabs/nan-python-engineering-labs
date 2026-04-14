import ast


def count_nodes(source: str) -> int:
    tree = ast.parse(source)
    return sum(1 for _ in ast.walk(tree))


def main() -> None:
    print(count_nodes('x = 1\nprint(x)'))


if __name__ == '__main__':
    main()
