"""Event-Driven Architecture."""
class EventBus:
    def __init__(self):
        self.handlers = {}
    def subscribe(self, t, h):
        if t not in self.handlers:
            self.handlers[t] = []
        self.handlers[t].append(h)
    def publish(self, event):
        for h in self.handlers.get(event.get("type"), []):
            h(event)

class OrderService:
    def __init__(self, bus):
        self.bus = bus
    def create(self, id):
        print(f"Order {id} created")
        self.bus.publish({"type": "order.created", "id": id})

def notify(evt):
    print(f"✓ Notification: {evt['id']}")

if __name__ == "__main__":
    bus = EventBus()
    bus.subscribe("order.created", notify)
    OrderService(bus).create("1")
    print("✓ Event-Driven")
