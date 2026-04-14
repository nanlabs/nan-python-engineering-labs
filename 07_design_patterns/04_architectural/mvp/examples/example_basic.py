class View:
    def show(self, text: str) -> str:
        return text


class Presenter:
    def __init__(self, view: View) -> None:
        self.view = view

    def present(self, data: str) -> str:
        return self.view.show(f'presented:{data}')


def main() -> None:
    print(Presenter(View()).present('stats'))


if __name__ == '__main__':
    main()
