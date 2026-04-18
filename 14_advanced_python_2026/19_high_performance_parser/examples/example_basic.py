"""Parse log lines efficiently and compute aggregate metrics with stdlib tools."""

from __future__ import annotations

import re
from statistics import mean
from time import perf_counter


LOG_LINES = [
    "2026-01-05T10:00:00Z level=INFO user=alice latency_ms=12 endpoint=/health",
    "2026-01-05T10:00:01Z level=INFO user=bob latency_ms=35 endpoint=/orders",
    "2026-01-05T10:00:02Z level=ERROR user=alice latency_ms=58 endpoint=/checkout",
    "2026-01-05T10:00:03Z level=INFO user=carol latency_ms=22 endpoint=/orders",
]

PATTERN = re.compile(
    r"^(?P<ts>\S+) level=(?P<level>\w+) user=(?P<user>\w+) "
    r"latency_ms=(?P<latency>\d+) endpoint=(?P<endpoint>/\w+)$"
)


def parse_line(line: str) -> dict[str, str | int]:
    match = PATTERN.match(line)
    if not match:
        raise ValueError(f"Invalid log line: {line}")
    data = match.groupdict()
    data["latency"] = int(data["latency"])
    return data


def main() -> None:
    t0 = perf_counter()
    parsed = [parse_line(line) for line in LOG_LINES]
    elapsed_us = (perf_counter() - t0) * 1_000_000

    latencies = [entry["latency"] for entry in parsed]
    errors = [entry for entry in parsed if entry["level"] == "ERROR"]

    print(f"Parsed {len(parsed)} log lines in {elapsed_us:.1f} µs")
    print(f"Average latency: {mean(latencies):.1f} ms")
    print(f"Error count: {len(errors)}")


if __name__ == "__main__":
    main()
