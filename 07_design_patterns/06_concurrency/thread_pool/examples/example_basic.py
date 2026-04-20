"""Thread pool example: process CPU-lite tasks concurrently."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            return False
        factor += 2
    return True


def main() -> None:
    """Entry point to demonstrate the implementation."""
    numbers = [101, 103, 107, 109, 221, 997, 1009, 1024]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(is_prime, n): n for n in numbers}
        for future in as_completed(futures):
            n = futures[future]
            print(f"{n}: {'prime' if future.result() else 'not prime'}")


if __name__ == "__main__":
    main()
