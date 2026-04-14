# Contract Testing

Estimated time: 2 hours

## Definition

Capture assumptions at service boundaries so consumers and providers can evolve without silent breakage.

## What You Practice

- Consumer contract
- Schema validation
- Provider expectations
- Backward compatibility

## Practical Applications

- REST responses
- event payloads
- internal service agreements

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply contract testing in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Validate a payment payload contract before business logic consumes it.

Success criteria:
- Implement `validate_payment_response`.
- Ensure required keys exist.
- Normalize statuses to lowercase.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

