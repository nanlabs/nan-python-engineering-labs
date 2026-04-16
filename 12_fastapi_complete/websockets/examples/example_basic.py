"""
Basic example: WebSockets
===========================

FastAPI supports WebSocket connections natively, enabling full-duplex,
real-time communication between the server and connected clients.

This example demonstrates:
1. Basic WebSocket echo server
2. Multi-client chat room with broadcast
3. WebSocket with authentication (token in query param)
4. Connection lifecycle management (connect, receive, disconnect)
5. Binary message support

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs  (for REST endpoints)

Test with wscat or the browser console:
    wscat -c "ws://localhost:8000/ws/public"
    wscat -c "ws://localhost:8000/ws/chat/room1?token=abc123&username=alice"
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException, status
from pydantic import BaseModel


# =============================================================================
# CONNECTION MANAGER
# =============================================================================


class ConnectionManager:
    """
    Manages active WebSocket connections per chat room.

    - Tracks connections by room name.
    - Broadcasts messages to all participants in a room.
    - Handles graceful disconnection cleanup.
    """

    def __init__(self):
        # room_name → {(websocket, username)}
        self._rooms: Dict[str, List[tuple[WebSocket, str]]] = {}

    async def connect(self, websocket: WebSocket, room: str, username: str):
        await websocket.accept()
        if room not in self._rooms:
            self._rooms[room] = []
        self._rooms[room].append((websocket, username))
        await self.broadcast(room, f"{username} joined the room.", sender="system")

    def disconnect(self, websocket: WebSocket, room: str, username: str):
        if room in self._rooms:
            self._rooms[room] = [
                (ws, u) for ws, u in self._rooms[room] if ws is not websocket
            ]

    async def broadcast(self, room: str, message: str, sender: str = "system"):
        """Send a message to every connection in the room."""
        payload = json.dumps({
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "room": room,
        })
        if room in self._rooms:
            dead = []
            for ws, username in self._rooms[room]:
                try:
                    await ws.send_text(payload)
                except Exception:
                    dead.append((ws, username))
            for item in dead:
                self._rooms[room].remove(item)

    async def send_personal(self, websocket: WebSocket, message: str):
        """Send a message to a single connection."""
        await websocket.send_text(json.dumps({
            "type": "personal",
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }))

    def room_members(self, room: str) -> List[str]:
        return [u for _, u in self._rooms.get(room, [])]

    def stats(self) -> dict:
        return {
            "rooms": list(self._rooms.keys()),
            "connections": {r: len(c) for r, c in self._rooms.items()},
            "total": sum(len(c) for c in self._rooms.values()),
        }


manager = ConnectionManager()

# Simple token store
VALID_TOKENS: dict[str, str] = {
    "abc123": "alice",
    "xyz789": "bob",
    "qwe456": "charlie",
}


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="WebSockets Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "WebSockets Demo", "docs": "/docs", "ws": "/ws/..."}


# ── 1. Echo WebSocket — simplest possible example ────────────────────────────


@app.websocket("/ws/echo")
async def echo_websocket(websocket: WebSocket):
    """
    Echo server — sends back whatever it receives.

    Connect: wscat -c "ws://localhost:8000/ws/echo"
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass


# ── 2. Public broadcast room ──────────────────────────────────────────────────


@app.websocket("/ws/public")
async def public_room(websocket: WebSocket, username: str = Query("anonymous")):
    """
    Public chat room — no authentication required.

    Connect: wscat -c "ws://localhost:8000/ws/public?username=alice"
    Messages are broadcast to all connected clients.
    """
    await manager.connect(websocket, "public", username)
    try:
        while True:
            text = await websocket.receive_text()
            await manager.broadcast("public", text, sender=username)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "public", username)
        await manager.broadcast("public", f"{username} left the room.", sender="system")


# ── 3. Private rooms with token authentication ───────────────────────────────


@app.websocket("/ws/chat/{room_name}")
async def private_room(
    websocket: WebSocket,
    room_name: str,
    token: str = Query(..., description="Auth token"),
):
    """
    Authenticated private chat room.

    - Token is validated before accepting the WebSocket connection.
    - Invalid tokens get a 403 close code.

    Connect: wscat -c "ws://localhost:8000/ws/chat/dev?token=abc123"
    """
    username = VALID_TOKENS.get(token)
    if not username:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, room_name, username)
    try:
        while True:
            message = await websocket.receive_text()
            # Support /quit command
            if message.strip().lower() == "/quit":
                await manager.send_personal(websocket, "Goodbye!")
                break
            await manager.broadcast(room_name, message, sender=username)
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, room_name, username)
        await manager.broadcast(room_name, f"{username} disconnected.", sender="system")


# ── 4. Binary WebSocket (e.g. file chunks) ────────────────────────────────────


@app.websocket("/ws/binary")
async def binary_websocket(websocket: WebSocket):
    """
    Binary WebSocket — receives bytes and echoes a summary.

    Useful for streaming file chunks or binary sensor data.
    Connect: wscat -c "ws://localhost:8000/ws/binary" --binary
    """
    await websocket.accept()
    total_bytes = 0
    try:
        while True:
            data = await websocket.receive_bytes()
            total_bytes += len(data)
            summary = json.dumps({
                "chunk_size": len(data),
                "total_received": total_bytes,
                "timestamp": datetime.now().isoformat(),
            })
            await websocket.send_text(summary)
    except WebSocketDisconnect:
        pass


# ── 5. REST endpoint — room statistics ──────────────────────────────────────


@app.get("/ws/stats")
async def ws_stats():
    """Return current WebSocket connection statistics."""
    return manager.stats()


@app.get("/ws/rooms/{room_name}/members")
async def room_members(room_name: str):
    """List current members of a chat room."""
    members = manager.room_members(room_name)
    return {"room": room_name, "members": members, "count": len(members)}


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 60)
    print("WEBSOCKETS — DEMO")
    print("=" * 60)
    print()
    print("WebSocket endpoints:")
    print("  ws://localhost:8000/ws/echo")
    print("    → Echo server — no auth required")
    print()
    print("  ws://localhost:8000/ws/public?username=alice")
    print("    → Public broadcast room")
    print()
    print("  ws://localhost:8000/ws/chat/myroom?token=abc123")
    print("    → Authenticated private room")
    print("    Valid tokens: abc123 (alice), xyz789 (bob), qwe456 (charlie)")
    print()
    print("  ws://localhost:8000/ws/binary")
    print("    → Binary message handler")
    print()
    print("REST endpoints:")
    print("  GET /ws/stats              — connection statistics")
    print("  GET /ws/rooms/{name}/members — room member list")
    print()
    print("Test with wscat:")
    print('  wscat -c "ws://localhost:8000/ws/public?username=alice"')
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    demo()
