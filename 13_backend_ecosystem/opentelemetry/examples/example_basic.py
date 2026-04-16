"""Basic example: spans inside one trace."""
import time
import uuid
from contextlib import contextmanager

@contextmanager
def span(trace_id, name):
    start = time.perf_counter()
    sid = uuid.uuid4().hex[:12]
    print('start', trace_id, sid, name)
    try:
        yield
    finally:
        print('end', trace_id, sid, name, f'ms={(time.perf_counter()-start)*1000:.2f}')

trace = uuid.uuid4().hex
with span(trace, 'http.request'):
    with span(trace, 'db.query'):
        time.sleep(0.02)
    with span(trace, 'cache.put'):
        time.sleep(0.01)
