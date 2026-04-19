"""Exercise: Contract Testing.

Goal:
Create `my_solution/payment_contract.py`.

Requirements:
- `validate_payment_response(payload)` ensures required fields exist.
- Required keys: `payment_id`, `status`, `amount`, `currency`.
- Return a normalized copy of the payload with lowercase status.
- Raise `ValueError` when keys are missing.

The baseline tests model a consumer-side contract.
"""
