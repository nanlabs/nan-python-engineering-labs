class TemperatureController:
    def __init__(self) -> None:
        self.__target = 22.0

    def set_target(self, value: float) -> None:
        if value < 16 or value > 30:
            raise ValueError("Target out of range")
        self.__target = value

    def get_target(self) -> float:
        return self.__target


def main() -> None:
    """Entry point to demonstrate the implementation."""
    controller = TemperatureController()
    controller.set_target(24.5)
    print(controller.get_target())


if __name__ == "__main__":
    main()
