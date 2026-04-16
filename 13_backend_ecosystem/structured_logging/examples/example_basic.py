"""Basic example: JSON logs with correlation id."""
import json
from datetime import datetime, timezone

def log(level, message, cid):
    print(json.dumps({'ts': datetime.now(timezone.utc).isoformat(), 'level': level, 'message': message, 'cid': cid}))

log('INFO', 'request started', 'req-100')
log('INFO', 'cache miss', 'req-100')
log('INFO', 'request completed', 'req-100')
