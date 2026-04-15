"""Vectorization concept without external dependencies."""


def scalar_transform(values: list[int]) -> list[int]:
    out: list[int] = []
    for v in values:
        out.append(v * v + 3 * v)
    return out


def vector_like_transform(values: list[int]) -> list[int]:
    return [v * v + 3 * v for v in values]


def main() -> None:
    values = list(range(20))
    print(f"Scalar first 5:    {scalar_transform(values)[:5]}")
    print(f"Vector-like first 5: {vector_like_transform(values)[:5]}")


if __name__ == '__main__':
    main()
