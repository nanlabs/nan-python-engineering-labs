"""Use Literal types to constrain valid values."""

from typing import Literal

LogLevel = Literal["debug", "info", "warning", "error"]


def format_log(level: LogLevel, message: str) -> str:
    prefix = {"debug": "DBG", "info": "INF", "warning": "WRN", "error": "ERR"}[level]
    return f"[{prefix}] {message}"


def main() -> None:
    print(format_log("info", "Server started"))


if __name__ == "__main__":
    main()
