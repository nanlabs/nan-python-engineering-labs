"""Basic example: queue with ack and retry."""
from collections import deque

q = deque(['job-a', 'job-b', 'job-c'])
while q:
    job = q.popleft()
    if job == 'job-b':
        print('retry', job)
        q.append('job-b-retry')
        continue
    print('ack', job)
