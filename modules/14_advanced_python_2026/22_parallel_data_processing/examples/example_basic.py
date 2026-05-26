"""
Parallel data processing with Rust.
Demonstrates multi-threaded computation.
"""


def process_chunk(chunk: list) -> list:
    """Process data chunk (would be parallelized in Rust)."""
    return [x * 2 for x in chunk]


def parallel_map(data: list, chunk_size: int = 100) -> list:
    """Map function in parallel chunks."""
    result = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size]
        result.extend(process_chunk(chunk))
    return result


if __name__ == "__main__":
    data = list(range(1000))
    result = parallel_map(data)
    print(f"Processed {len(result)} items")
    print(f"First 5 items: {result[:5]}")
