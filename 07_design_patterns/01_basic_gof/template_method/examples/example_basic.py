"""Template Method example: fixed parsing pipeline with custom steps."""
from __future__ import annotations
from abc import ABC, abstractmethod

class DataParser(ABC):
    def parse(self, raw: str) -> list[dict[str, str]]:
        lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
        header = self._extract_header(lines[0])
        rows = [self._extract_values(line) for line in lines[1:]]
        return [dict(zip(header, row, strict=True)) for row in rows]

    @abstractmethod
    def _extract_header(self, line: str) -> list[str]: ...

    @abstractmethod
    def _extract_values(self, line: str) -> list[str]: ...

class CsvParser(DataParser):
    def _extract_header(self, line: str) -> list[str]:
        return [item.strip() for item in line.split(",")]
    def _extract_values(self, line: str) -> list[str]:
        return [item.strip() for item in line.split(",")]

class PipeParser(DataParser):
    def _extract_header(self, line: str) -> list[str]:
        return [item.strip().lower() for item in line.split("|")]
    def _extract_values(self, line: str) -> list[str]:
        return [item.strip() for item in line.split("|")]

def main() -> None:
    csv_data = """name, role
Alice, Engineer
Bob, Designer"""
    pipe_data = """Name | Team
Carol | Platform
Dan | Security"""
    print("CSV :", CsvParser().parse(csv_data))
    print("PIPE:", PipeParser().parse(pipe_data))

if __name__ == "__main__":
    main()
