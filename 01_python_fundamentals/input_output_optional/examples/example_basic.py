"""Working example of input and output without real user input."""


def parse_csv_line(raw_line: str) -> tuple[str, int, str]:
    """Transform a simple comma-separated line into typed values."""
    name, age, city = [part.strip() for part in raw_line.split(",")]
    return name, int(age), city


def format_receipt(name: str, total: float) -> str:
    """Generate multiline output ready to print or save."""
    return f"Customer: {name}\nTotal: ${total:.2f}\nStatus: confirmed"


def main() -> None:
    customer = parse_csv_line("Grace Hopper, 37, New York")
    print(customer)
    print(format_receipt(customer[0], 149.99))


if __name__ == "__main__":
    main()
