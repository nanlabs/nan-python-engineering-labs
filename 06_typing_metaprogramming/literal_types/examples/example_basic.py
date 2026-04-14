from typing import Literal


Mode = Literal['read', 'write']


def open_mode(mode: Mode) -> str:
    return f'mode={mode}'


def main() -> None:
    print(open_mode('read'))


if __name__ == '__main__':
    main()
