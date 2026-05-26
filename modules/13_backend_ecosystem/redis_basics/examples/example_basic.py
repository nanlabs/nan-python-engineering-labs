"""Basic example: get/set/incr with TTL semantics."""

import time

store = {}


def set_value(key, value, ttl=None):
    exp = time.time() + ttl if ttl else None
    store[key] = (value, exp)


def get_value(key):
    value, exp = store.get(key, (None, None))
    if exp and time.time() >= exp:
        store.pop(key, None)
        return None
    return value


def incr(key):
    value = int(get_value(key) or "0") + 1
    set_value(key, str(value))
    return value


set_value("service", "backend", ttl=1)
print(get_value("service"))
print(incr("hits"))
print(incr("hits"))
time.sleep(1.1)
print(get_value("service"))
