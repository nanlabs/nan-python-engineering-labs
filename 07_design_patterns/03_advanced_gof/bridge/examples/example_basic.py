class Device:
    def enable(self) -> str:
        raise NotImplementedError


class TV(Device):
    def enable(self) -> str:
        return 'tv:on'


class Radio(Device):
    def enable(self) -> str:
        return 'radio:on'


class Remote:
    def __init__(self, device: Device) -> None:
        self.device = device

    def turn_on(self) -> str:
        return self.device.enable()


def main() -> None:
    print(Remote(Radio()).turn_on())


if __name__ == '__main__':
    main()
