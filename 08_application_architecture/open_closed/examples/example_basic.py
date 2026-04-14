"""Open/Closed - open for extension, closed for modification."""
from abc import ABC, abstractmethod

class Formatter(ABC):
    @abstractmethod
    def format(self, data): pass

class JsonFormatter(Formatter):
    def format(self, data): return f'JSON: {data}'

class CsvFormatter(Formatter):
    def format(self, data): return f'CSV: {data}'

class Report:
    def __init__(self, fmt): self.fmt = fmt
    def generate(self, data): return self.fmt.format(data)

if __name__ == "__main__":
    print(Report(JsonFormatter()).generate("data"))
    print("✓ Open/Closed")
