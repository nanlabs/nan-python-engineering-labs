from multiprocessing import Array


def main() -> None:
    shared = Array('i', [1, 2, 3])
    shared[0] = 10
    print(list(shared))


if __name__ == '__main__':
    main()
