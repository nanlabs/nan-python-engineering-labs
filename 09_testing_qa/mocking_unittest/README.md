# Mocking with unittest.mock

Estimated time: 2-3 hours

## Definition

Isolate outbound calls with `unittest.mock` so business rules can be tested without real integrations.

## What You Practice

- Mock
- Patch
- Autospec
- Assert_called_once_with

## Practical Applications

- SMTP clients
- HTTP gateways
- payment processors

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply mocking with unittest.mock in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement a notifier that delegates delivery to an injected gateway.

Success criteria:
- Create a `Notification` dataclass.
- Create `Notifier.send_welcome_email`.
- Return `False` instead of propagating gateway failures.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

