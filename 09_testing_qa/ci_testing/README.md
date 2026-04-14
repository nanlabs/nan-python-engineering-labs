# CI Testing

Estimated time: 2 hours

## Definition

Design tests and reporting so continuous integration can gate merges with confidence.

## What You Practice

- Quality gates
- Report parsing
- Failing fast
- Artifact generation

## Practical Applications

- Pull request validation
- nightly builds
- release promotion

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply ci testing in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement quality-gate logic that a CI job could evaluate automatically.

Success criteria:
- Implement `validate_test_report`.
- Implement `should_publish_artifacts`.
- Reject malformed report payloads.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

