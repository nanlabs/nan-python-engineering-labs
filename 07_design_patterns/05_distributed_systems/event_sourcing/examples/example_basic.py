from dataclasses import dataclass


@dataclass
class PatternCard:
    name: str
    category: str
    purpose: str


def build_pattern_card() -> PatternCard:
    return PatternCard(
        name='Event Sourcing',
        category='05 Distributed Systems',
        purpose='Demonstrate the core structure of the pattern in Python.'
    )


def main() -> None:
    card = build_pattern_card()
    print(f"{card.name} | {card.category}")
    print(card.purpose)


if __name__ == '__main__':
    main()
