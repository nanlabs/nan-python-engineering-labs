# Hypothesis Introduction

Estimated time: 2-3 hours

## Definition

Generate inputs automatically and let Hypothesis discover surprising cases you would not handwrite.

## What You Practice

- Strategies
- Property discovery
- Shrinking
- State space exploration

## Practical Applications

- Parsing helpers
- normalization utilities
- pure functions

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply hypothesis introduction in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement a text normalizer with properties that hold for a wide input space.

Success criteria:
- Implement `collapse_whitespace`.
- Implement `normalize_title`.
- Make both functions idempotent.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

