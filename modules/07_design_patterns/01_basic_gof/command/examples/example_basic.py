"""Command pattern example: decouple button actions from receivers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Light:
    location: str
    is_on: bool = False

    def turn_on(self) -> str:
        self.is_on = True
        return f"{self.location} light is ON"

    def turn_off(self) -> str:
        self.is_on = False
        return f"{self.location} light is OFF"


class Command:
    def execute(self) -> str:
        ...

    def undo(self) -> str:
        ...


@dataclass
class TurnOnLight(Command):
    light: Light

    def execute(self) -> str:
        return self.light.turn_on()

    def undo(self) -> str:
        return self.light.turn_off()


@dataclass
class TurnOffLight(Command):
    light: Light

    def execute(self) -> str:
        return self.light.turn_off()

    def undo(self) -> str:
        return self.light.turn_on()


class RemoteControl:
    def __init__(self) -> None:
        self._history: list[Command] = []

    def press(self, command: Command) -> str:
        result = command.execute()
        self._history.append(command)
        return result

    def undo_last(self) -> str:
        if not self._history:
            return "Nothing to undo"
        return self._history.pop().undo()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    living_room = Light("Living room")
    remote = RemoteControl()
    print(remote.press(TurnOnLight(living_room)))
    print(remote.press(TurnOffLight(living_room)))
    print(remote.undo_last())
    print(f"Final state: {'ON' if living_room.is_on else 'OFF'}")


if __name__ == "__main__":
    main()
