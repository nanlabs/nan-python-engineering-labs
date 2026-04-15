def safe_eval(expression: str) -> int:
    code = compile(expression, "<expr>", "eval")
    return eval(code, {}, {})


def evaluate_many(expressions: list[str]) -> list[int]:
    return [safe_eval(expr) for expr in expressions]


def main() -> None:
    batch = ["2 + 3 * 4", "10 - 2", "8 // 2"]
    print(evaluate_many(batch))


if __name__ == "__main__":
    main()
