from multiprocessing import Array


def increment_shared(shared: Array) -> None:
    for index in range(len(shared)):
        shared[index] += 1


def main() -> None:
    shared = Array("i", [1, 2, 3])
    increment_shared(shared)
    print(list(shared))


if __name__ == "__main__":
    main()
