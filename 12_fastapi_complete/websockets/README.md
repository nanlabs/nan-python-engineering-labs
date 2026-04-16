# WebSockets

Estimated time: 2 hours

## 1. Definition

**WebSockets** provide a persistent, full-duplex TCP connection between client and server, enabling real-time bidirectional communication without the overhead of HTTP polling. FastAPI supports WebSockets natively via the `@app.websocket()` decorator.

### Key Characteristics

- **Persistent connection**: unlike HTTP, the connection stays open after the initial handshake.
- **Full-duplex**: server and client can send messages at any time independently.
- **`WebSocketDisconnect`**: exception raised when the client closes the connection.
- **`await websocket.receive_text()` / `send_text()`**: async message exchange.
- **Connection management**: a `ConnectionManager` class is the standard pattern for multi-client scenarios.

## 2. Practical Application

### Use Cases

- Real-time chat applications with multiple rooms.
- Live dashboard updates (prices, metrics, notifications).
- Collaborative editing (document cursors, presence).
- Streaming server-side events to browser clients.

### Code Example

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/echo")
async def echo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f"Echo: {text}")
    except WebSocketDisconnect:
        pass
```

## 3. Why Is It Important?

### Problem It Solves

HTTP polling (client asks the server every N seconds "anything new?") wastes bandwidth and adds latency. Server-sent events are unidirectional. WebSockets are the correct primitive for low-latency bidirectional data.

### Solution and Benefits

WebSockets eliminate polling entirely. The server pushes data the instant it is available. One persistent connection replaces hundreds of HTTP requests per minute.

## 4. References

- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a WebSocket echo endpoint at `/ws/echo`. Send any message; receive it back prefixed with `"Echo: "`.

### Intermediate Level

Create a chat room at `/ws/chat/{room}` using a `ConnectionManager` that broadcasts every message to all connected clients in the same room.

### Advanced Level

Add token authentication to `/ws/chat/{room}?token=...`. Reject invalid tokens with close code `1008`. Track members per room and expose `GET /rooms/{room}/members`.

### Success Criteria

- Echo endpoint responds immediately to every message.
- Multiple clients in the same room all receive broadcast messages.
- Invalid token closes the connection with code 1008.

## 6. Summary

FastAPI WebSockets provide full-duplex real-time communication with native async support. The `WebSocketDisconnect` exception handles client disconnections cleanly. A `ConnectionManager` class is the idiomatic pattern for multi-client broadcast.

## 7. Reflection Prompt

WebSockets maintain a persistent server-side state per connection. How does this affect horizontal scaling across multiple server instances? What infrastructure would you need to broadcast to clients connected on different servers?
