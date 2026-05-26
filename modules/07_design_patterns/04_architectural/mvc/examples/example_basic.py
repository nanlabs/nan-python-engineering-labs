class Model:
    def __init__(self) -> None:
        self.value = "hello"


class View:
    def render(self, text: str) -> str:
        return text.upper()


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

    def handle(self) -> str:
        return self.view.render(self.model.value)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(Controller(Model(), View()).handle())


if __name__ == "__main__":
    main()
