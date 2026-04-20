"""Basic example: counters and histogram buckets exposition."""

import random

req_total = 0
err_total = 0
buckets = {0.05: 0, 0.1: 0, 0.25: 0, 1.0: 0}

for i in range(10):
    req_total += 1
    latency = random.choice([0.03, 0.08, 0.12, 0.30])
    if i % 4 == 0:
        err_total += 1
    for b in sorted(buckets):
        if latency <= b:
            buckets[b] += 1
            break

print("# TYPE app_requests_total counter")
print(f"app_requests_total {req_total}")
print("# TYPE app_errors_total counter")
print(f"app_errors_total {err_total}")
for b, c in buckets.items():
    print(f'app_request_latency_seconds_bucket{{le="{b}"}} {c}')
