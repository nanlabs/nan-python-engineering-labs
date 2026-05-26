from dataclasses import dataclass


@dataclass
class PEPFact:
    number: int
    topic: str


def pep_703_summary() -> PEPFact:
    return PEPFact(number=703, topic="Optional GIL in CPython")


def main() -> None:
    """Entry point to demonstrate the implementation."""
    summary = pep_703_summary()
    print(f"PEP {summary.number}: {summary.topic}")


if __name__ == "__main__":
    main()
