def safe_eval(expression: str) -> int:
    code = compile(expression, '<expr>', 'eval')
    return eval(code, {}, {})


def main() -> None:
    print(safe_eval('2 + 3 * 4'))


if __name__ == '__main__':
    main()
