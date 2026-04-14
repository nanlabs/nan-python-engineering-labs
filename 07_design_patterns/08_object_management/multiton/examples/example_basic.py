class LoggerMultiton:
    _instances: dict[str, 'LoggerMultiton'] = {}

    def __new__(cls, channel: str):
        if channel not in cls._instances:
            inst = super().__new__(cls)
            inst.channel = channel
            cls._instances[channel] = inst
        return cls._instances[channel]


def main() -> None:
    a = LoggerMultiton('api')
    b = LoggerMultiton('api')
    c = LoggerMultiton('worker')
    print(a is b, a is c)


if __name__ == '__main__':
    main()
