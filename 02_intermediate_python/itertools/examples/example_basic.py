"""Working example of itertools."""

from itertools import accumulate, chain, pairwise


def main() -> None:
    print(list(chain(['a', 'b'], ['c'])))
    print(list(accumulate([1, 2, 3, 4])))
    print(list(pairwise([10, 20, 30, 40])))


if __name__ == '__main__':
    main()
