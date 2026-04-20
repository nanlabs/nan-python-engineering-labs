"""Basic example: cache-aside and write-through update."""

import time

db = {1: {"id": 1, "name": "Keyboard", "price": 99.0}}
cache = {}


def read_product(pid):
    key = f"p:{pid}"
    if key in cache:
        return "HIT", cache[key]
    time.sleep(0.05)
    cache[key] = db[pid].copy()
    return "MISS", cache[key]


def update_price(pid, price):
    db[pid]["price"] = price
    cache[f"p:{pid}"] = db[pid].copy()


print(read_product(1))
print(read_product(1))
update_price(1, 89.0)
print(read_product(1))
