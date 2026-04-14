class Button:
    def render(self) -> str:
        raise NotImplementedError


class LinuxButton(Button):
    def render(self) -> str:
        return 'linux-button'


class WindowsButton(Button):
    def render(self) -> str:
        return 'windows-button'


class UIFactory:
    def button(self) -> Button:
        raise NotImplementedError


class LinuxFactory(UIFactory):
    def button(self) -> Button:
        return LinuxButton()


class WindowsFactory(UIFactory):
    def button(self) -> Button:
        return WindowsButton()


def main() -> None:
    print(LinuxFactory().button().render())


if __name__ == '__main__':
    main()
