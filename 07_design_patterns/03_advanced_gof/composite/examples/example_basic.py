class Node:
    def total(self) -> int:
        raise NotImplementedError


class Leaf(Node):
    def __init__(self, value: int) -> None:
        self.value = value

    def total(self) -> int:
        return self.value


class Branch(Node):
    def __init__(self, children: list[Node]) -> None:
        self.children = children

    def total(self) -> int:
        return sum(child.total() for child in self.children)


def main() -> None:
    tree = Branch([Leaf(2), Branch([Leaf(3), Leaf(4)])])
    print(tree.total())


if __name__ == '__main__':
    main()
