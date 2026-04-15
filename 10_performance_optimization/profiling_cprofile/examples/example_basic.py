"""Basic cProfile example for hotspot discovery."""

import cProfile
import pstats


def build_report(n: int) -> int:
    total = 0
    for i in range(n):
        total += sum(j * j for j in range(i % 200))
    return total


def main() -> None:
    profiler = cProfile.Profile()
    profiler.enable()
    value = build_report(2000)
    profiler.disable()

    print(f"Computed value: {value}")
    stats = pstats.Stats(profiler).strip_dirs().sort_stats('cumtime')
    stats.print_stats(5)


if __name__ == '__main__':
    main()
