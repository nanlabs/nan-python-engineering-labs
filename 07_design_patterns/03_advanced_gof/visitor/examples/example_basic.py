class Number:
    def __init__(self, value: int) -> None:
        self.value = value

    def accept(self, visitor) -> int:
        return visitor.visit_number(self)


class SumVisitor:
    def __init__(self) -> None:
        self.total = 0

    def visit_number(self, node: Number) -> int:
        self.total += node.value
        return self.total


def main() -> None:
    visitor = SumVisitor()
    for n in [Number(1), Number(4), Number(5)]:
        n.accept(visitor)
    print(visitor.total)


if __name__ == '__main__':
    main()
