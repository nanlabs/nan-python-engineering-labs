import threading


def main() -> None:
    barrier = threading.Barrier(3)
    out: list[str] = []

    def worker(name: str) -> None:
        out.append(f'ready:{name}')
        barrier.wait()
        out.append(f'run:{name}')

    threads = [threading.Thread(target=worker, args=(f'w{i}',)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(sorted(out))


if __name__ == '__main__':
    main()
