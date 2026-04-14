from typing import Optional


def normalize_name(value: Optional[str]) -> str:
    return value.strip().title() if value else 'Unknown'


def main() -> None:
    print(normalize_name('  lin  '))
    print(normalize_name(None))


if __name__ == '__main__':
    main()
