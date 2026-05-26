"""Working example of CSV and JSON processing."""

import csv
import json
from io import StringIO


def load_sales_from_csv(raw_csv: str) -> list[dict[str, str]]:
    """Parse CSV text into dictionaries."""
    return list(csv.DictReader(StringIO(raw_csv)))


def sales_to_json(rows: list[dict[str, str]]) -> str:
    """Serialize parsed rows to formatted JSON."""
    return json.dumps(rows, indent=2)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    raw_csv = "name,amount\nAda,120\nLin,95\n"
    sales = load_sales_from_csv(raw_csv)
    print(sales)
    print(sales_to_json(sales))


if __name__ == "__main__":
    main()
