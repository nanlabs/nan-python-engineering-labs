import heapq


def main() -> None:
    schedule: list[tuple[int, str]] = []
    heapq.heappush(schedule, (20, 'nightly-job'))
    heapq.heappush(schedule, (10, 'health-check'))
    print(heapq.heappop(schedule))


if __name__ == '__main__':
    main()
