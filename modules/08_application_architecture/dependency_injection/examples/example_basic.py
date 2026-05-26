"""Dependency Injection - inject dependencies."""


class Logger:
    def log(self, msg):
        print(f"[LOG] {msg}")


class Service:
    def __init__(self, logger: Logger):
        self.logger = logger

    def do_work(self):
        self.logger.log("Working...")


if __name__ == "__main__":
    svc = Service(Logger())
    svc.do_work()
    print("✓ Dependency Injection")
