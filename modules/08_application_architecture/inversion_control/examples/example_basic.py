"""Inversion of Control - framework controls lifecycle."""


class Container:
    def __init__(self):
        self.services = {}

    def register(self, name, obj):
        self.services[name] = obj

    def get(self, name):
        return self.services.get(name)


class Logger:
    def log(self, msg):
        print(f"[LOG] {msg}")


class Service:
    def __init__(self, container):
        self.log = container.get("logger")


if __name__ == "__main__":
    c = Container()
    c.register("logger", Logger())
    s = Service(c)
    s.log.log("test")
    print("✓ IoC Container")
