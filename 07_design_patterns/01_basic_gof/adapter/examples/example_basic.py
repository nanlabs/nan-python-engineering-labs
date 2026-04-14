class LegacyTemperatureSensor:
    def read_fahrenheit(self) -> float:
        return 77.0


class CelsiusSensorAdapter:
    def __init__(self, legacy: LegacyTemperatureSensor) -> None:
        self.legacy = legacy

    def read_celsius(self) -> float:
        return (self.legacy.read_fahrenheit() - 32) * 5 / 9


def main() -> None:
    sensor = CelsiusSensorAdapter(LegacyTemperatureSensor())
    print(round(sensor.read_celsius(), 2))


if __name__ == '__main__':
    main()
