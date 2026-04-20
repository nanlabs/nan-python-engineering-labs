"""Single Responsibility - one reason to change."""


class Validator:
    def validate(self, data):
        return len(str(data)) > 0


class Repository:
    def save(self, data):
        print(f"Saved: {data}")


class Service:
    def __init__(self, validator, repo):
        self.v, self.r = validator, repo

    def process(self, data):
        if self.v.validate(data):
            self.r.save(data)


if __name__ == "__main__":
    s = Service(Validator(), Repository())
    s.process("test")
    print("✓ Single Responsibility")
