"""Observability - metrics and traces."""

import json
from time import time


class Metrics:
    def __init__(self):
        self.metrics = []

    def record(self, name, val, **labels):
        m = {"name": name, "value": val, "labels": labels}
        self.metrics.append(m)
        print(json.dumps(m))


class Tracer:
    def __init__(self, m):
        self.m = m

    def trace(self, op, fn):
        start = time()
        result = fn()
        dur = (time() - start) * 1000
        self.m.record(f"{op}.ms", dur, status="ok")
        return result


if __name__ == "__main__":
    m = Metrics()
    t = Tracer(m)
    t.trace("db.query", lambda: "data")
    print("✓ Observability")
