"""Basic example: pub/sub fan-out to subscribers."""
from collections import defaultdict

subs = defaultdict(list)

def subscribe(channel, fn):
    subs[channel].append(fn)

def publish(channel, message):
    for fn in subs[channel]:
        fn(message)

subscribe('orders', lambda m: print('billing:', m))
subscribe('orders', lambda m: print('shipping:', m))
publish('orders', 'order-created')
publish('orders', 'order-paid')
