"""Abstract Factory example: build matching UI components for each theme."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


class LightButton(Button):
    def render(self) -> str:
        return "[Light Button]"


class DarkButton(Button):
    def render(self) -> str:
        return "[Dark Button]"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "[Light Checkbox]"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "[Dark Checkbox]"


class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        ...


class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


def render_screen(factory: UIFactory) -> str:
    return f"{factory.create_button().render()} {factory.create_checkbox().render()}"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print("Light:", render_screen(LightThemeFactory()))
    print("Dark :", render_screen(DarkThemeFactory()))


if __name__ == "__main__":
    main()
