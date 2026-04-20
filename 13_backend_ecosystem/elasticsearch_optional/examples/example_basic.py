"""Basic example: tiny inverted index search."""

import re
from collections import defaultdict

docs = {
    1: "python backend observability with prometheus metrics",
    2: "redis caching patterns for backend services",
    3: "kafka streams and event driven architecture",
}
index = defaultdict(set)
for doc_id, text in docs.items():
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        index[token].add(doc_id)

query = "backend metrics redis"
scores = defaultdict(int)
for token in re.findall(r"[a-z0-9]+", query):
    for doc_id in index[token]:
        scores[doc_id] += 1

print(sorted(scores.items(), key=lambda x: x[1], reverse=True))
