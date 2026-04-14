import copy
from dataclasses import dataclass


@dataclass
class Report:
    title: str
    tags: list[str]


def main() -> None:
    base = Report('weekly', ['ops'])
    clone = copy.deepcopy(base)
    clone.tags.append('infra')
    print(base.tags, clone.tags)


if __name__ == '__main__':
    main()
