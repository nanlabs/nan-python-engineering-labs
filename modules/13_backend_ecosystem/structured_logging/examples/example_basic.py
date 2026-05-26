"""Emit structured JSON logs using Python's built-in logging package."""

from __future__ import annotations

import json
import logging
import time
from typing import Any


class JsonFormatter(logging.Formatter):
    """Format log records as one-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
        }
        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "duration_ms"):
            payload["duration_ms"] = record.duration_ms
        return json.dumps(payload, sort_keys=True)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    logger = logging.getLogger("structured-demo")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.handlers[:] = [handler]

    started = time.perf_counter()
    logger.info("Starting import pipeline", extra={"event": "pipeline_start"})

    time.sleep(0.03)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    logger.info(
        "Import pipeline completed",
        extra={"event": "pipeline_complete", "duration_ms": duration_ms},
    )


if __name__ == "__main__":
    main()
