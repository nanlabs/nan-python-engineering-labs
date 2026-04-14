# pytest-mock

Estimated time: 2 hours

## Definition

Use the `mocker` fixture to patch collaborators in a concise pytest-native style.

## What You Practice

- Mocker fixture
- Spy
- Stub
- Patch.object

## Practical Applications

- Service orchestration
- time-dependent code
- repository adapters

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply pytest-mock in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Build a service that collaborates with a repository and a clock dependency.

Success criteria:
- Implement `ReportService.generate_daily_summary`.
- Compose repository data with the current date.
- Raise `LookupError` when the repository has no data for a day.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

