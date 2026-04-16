"""Basic example: compact schema message encode/decode."""
import json
from dataclasses import asdict, dataclass

@dataclass
class Event:
    version: int
    user_id: int
    kind: str

raw = json.dumps(asdict(Event(1, 42, 'user.created')), separators=(',', ':')).encode()
decoded = Event(**json.loads(raw.decode()))

print('bytes=', len(raw))
print('decoded=', decoded)
