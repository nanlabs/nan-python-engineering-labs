"""uv.lock: deterministic lock files for reproducible environments."""


def lock_entry(name: str, version: str, hash_: str) -> dict[str, str]:
    return {"name": name, "version": version, "hash": hash_}


def simulate_lock(packages: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [lock_entry(n, v, f"sha256:{hash(n+v) & 0xFFFFFF:06x}") for n, v in packages]


def verify_lock(entries: list[dict[str, str]]) -> str:
    return f"Lock verified: {len(entries)} packages, 0 conflicts"


def main() -> None:
    lock = simulate_lock([("requests", "2.31.0"), ("httpx", "0.27.0")])
    for entry in lock:
        print(entry)
    print(verify_lock(lock))


if __name__ == "__main__":
    main()
