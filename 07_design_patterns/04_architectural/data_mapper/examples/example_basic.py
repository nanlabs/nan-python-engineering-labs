from dataclasses import dataclass


@dataclass
class PatternCard:
    name: str
    category: str
    purpose: str


def build_pattern_card() -> PatternCard:
    return PatternCard(
        name='Data Mapper',
        category='04 Architectural',
        purpose='Demonstrate the core structure of the pattern in Python.'
    )


def main() -> None:
    card = build_pattern_card()
    print(f"{card.name} | {card.category}")
    print(card.purpose)


if __name__ == '__main__':
    main()
