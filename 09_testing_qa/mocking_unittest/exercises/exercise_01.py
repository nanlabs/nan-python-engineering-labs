"""Exercise: Mocking with unittest.mock.

Goal:
Create `my_solution/notifier.py`.

Requirements:
- Add a `Notification` dataclass with `recipient`, `subject`, and `body`.
- Implement `Notifier(gateway)`.
- Implement `send_welcome_email(recipient)` that builds a notification and calls `gateway.deliver`.
- If the gateway raises `RuntimeError`, return `False`.

The provided tests use `Mock` and `patch` to verify collaboration behavior.
"""
