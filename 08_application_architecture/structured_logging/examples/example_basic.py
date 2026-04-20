"""Structured Logging - JSON format."""

import json
from datetime import datetime


class StructLog:
    def log(self, level, msg, **ctx):
        entry = {"ts": datetime.now().isoformat(), "level": level, "msg": msg, "ctx": ctx}
        print(json.dumps(entry))


class UserService:
    def __init__(self, log):
        self.log = log

    def register(self, id, email):
        self.log.log("INFO", "Reg start", user_id=id, email=email)
        self.log.log("INFO", "Reg done", status="ok")


if __name__ == "__main__":
    UserService(StructLog()).register(1, "a@x.com")
    print("✓ StructLog")
