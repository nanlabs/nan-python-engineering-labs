"""memray: memory profiling concepts demo."""


def allocate_data(n: int) -> list[dict[str, object]]:
    return [{"id": i, "value": i * 2, "label": f"item_{i}"} for i in range(n)]


def estimate_memory(items: list[dict[str, object]]) -> dict[str, int]:
    item_bytes = sum(
        len(str(k)) + len(str(v))
        for item in items
        for k, v in item.items()
    )
    return {"items": len(items), "estimated_bytes": item_bytes, "estimated_kb": item_bytes // 1024}


def main() -> None:
    data = allocate_data(1_000)
    stats = estimate_memory(data)
    print(stats)
    print("In production: use `python -m memray run -o output.bin script.py`")


if __name__ == "__main__":
    main()
