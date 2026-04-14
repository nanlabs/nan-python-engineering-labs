from dataclasses import dataclass


@dataclass
class Light:
    on: bool = False

    def turn_on(self) -> None:
        self.on = True

    def turn_off(self) -> None:
        self.on = False


class Command:
    def execute(self) -> None:
        raise NotImplementedError


class TurnOn(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.turn_on()


class TurnOff(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.turn_off()


def main() -> None:
    light = Light()
    TurnOn(light).execute()
    TurnOff(light).execute()
    print(light.on)


if __name__ == '__main__':
    main()
