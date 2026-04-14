"""Entities vs Value Objects - DDD concepts."""
class UserId:
    def __init__(self, v): self.value = v
    def __eq__(self, o): return self.value == o.value

class Email:
    def __init__(self, a): self.addr = a
    def valid(self): return "@" in self.addr

class User:
    def __init__(self, id, email):
        self.id, self.email = id, email

if __name__ == "__main__":
    u = User(UserId(1), Email("test@x.com"))
    print(f"✓ Entities/ValueObjects: {u.email.addr}")
