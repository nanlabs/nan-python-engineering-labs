"""Basic example: partitions and consumer offsets."""

from collections import defaultdict

partitions = defaultdict(list)
offsets = defaultdict(int)


def produce(key, value, n=3):
    p = hash(key) % n
    partitions[p].append(value)
    return p, len(partitions[p]) - 1


def poll(n=3):
    out = []
    for p in range(n):
        for i in range(offsets[p], len(partitions[p])):
            out.append((p, i, partitions[p][i]))
        offsets[p] = len(partitions[p])
    return out


print(produce("u1", "event-login"))
print(produce("u2", "event-cart"))
print(poll())
print(poll())
