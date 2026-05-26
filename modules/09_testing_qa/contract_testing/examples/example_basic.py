"""A contract is just a precise statement of expectations."""

from __future__ import annotations

REQUIRED_KEYS = {"payment_id", "status", "amount", "currency"}


def validate_payment_response(payload: dict[str, object]) -> dict[str, object]:
    missing = REQUIRED_KEYS - payload.keys()
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    normalized = dict(payload)
    normalized["status"] = str(payload["status"]).lower()
    return normalized


if __name__ == "__main__":
    payload = {
        "payment_id": "pay_123",
        "status": "APPROVED",
        "amount": 150.0,
        "currency": "USD",
    }
    print("contract testing example")
    print(validate_payment_response(payload))
