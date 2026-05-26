"""Open/Closed: extend behavior without modifying existing code."""

from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, data: dict[str, object]) -> str:
        ...


class JsonFormatter(Formatter):
    def format(self, data: dict[str, object]) -> str:
        return f"JSON: {data}"


class CsvFormatter(Formatter):
    def format(self, data: dict[str, object]) -> str:
        return f"CSV: {','.join(str(v) for v in data.values())}"


class Report:
    def __init__(self, fmt: Formatter):
        self.fmt = fmt

    def generate(self, data: dict[str, object]) -> str:
        return self.fmt.format(data)


if __name__ == "__main__":
    payload = {"id": 1, "name": "alice"}
    print(Report(JsonFormatter()).generate(payload))
    print(Report(CsvFormatter()).generate(payload))
