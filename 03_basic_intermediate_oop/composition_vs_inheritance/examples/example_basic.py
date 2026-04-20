class Engine:
    def start(self) -> str:
        return "Engine started"


class Car:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def drive(self) -> str:
        return f"{self.engine.start()} and car is moving"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    car = Car(Engine())
    print(car.drive())


if __name__ == "__main__":
    main()
