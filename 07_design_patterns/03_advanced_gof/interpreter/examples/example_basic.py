class Context(dict[str, int]):
    def lookup(self, name: str) -> int:
        return self[name]


class Expression:
    def interpret(self, ctx: Context) -> int:
        raise NotImplementedError("Subclasses must implement interpret")


class Number(Expression):
    def __init__(self, value: int) -> None:
        self.value = value

    def interpret(self, ctx: Context) -> int:
        return self.value


class Add(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def interpret(self, ctx: Context) -> int:
        return self.left.interpret(ctx) + self.right.interpret(ctx)


def main() -> None:
    expr = Add(Number(2), Number(5))
    print(expr.interpret(Context()))


if __name__ == "__main__":
    main()
