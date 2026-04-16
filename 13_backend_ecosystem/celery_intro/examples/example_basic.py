"""Basic example: task dispatch simulation."""
from time import sleep

def delay(name, payload):
    print('dispatched', name, payload)
    sleep(0.01)
    return {'task': name, 'status': 'SUCCESS', 'payload': payload}

print(delay('send_email', {'to': 'alice@example.com'}))
print(delay('generate_invoice', {'order_id': 91}))
