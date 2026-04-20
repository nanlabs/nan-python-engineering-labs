"""CPU-heavy workload sample intended for py-spy inspection."""


def compute_primes(limit: int) -> list[int]:
    primes: list[int] = []
    for n in range(2, limit):
        is_prime = True
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(n)
    return primes


def main() -> None:
    """Entry point to demonstrate the implementation."""
    primes = compute_primes(10000)
    print(f"Prime count: {len(primes)}")
    print("Tip: run this file with py-spy to inspect sampling output.")


if __name__ == "__main__":
    main()
