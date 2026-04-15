"""Pure Python baseline before moving critical code to Cython."""


def dot_product(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def main() -> None:
    a = [float(i) for i in range(1, 1001)]
    b = [float(i) / 3.0 for i in range(1, 1001)]
    print(f"Dot product baseline: {dot_product(a, b):.2f}")
    print('This function is a good candidate for Cython acceleration.')


if __name__ == '__main__':
    main()
