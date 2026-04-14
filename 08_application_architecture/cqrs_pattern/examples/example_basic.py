"""CQRS - separate command and query."""
class CreateUserCmd:
    def __init__(self, id, name):
        self.id, self.name = id, name

class CmdHandler:
    def __init__(self):
        self.db = {}
    def handle(self, cmd):
        self.db[cmd.id] = {"id": cmd.id, "name": cmd.name}

class QryHandler:
    def __init__(self, db):
        self.db = db
    def get_user(self, id):
        return self.db.get(id)

if __name__ == "__main__":
    h = CmdHandler()
    h.handle(CreateUserCmd(1, "alice"))
    q = QryHandler(h.db)
    print(f"✓ CQRS: {q.get_user(1)}")
