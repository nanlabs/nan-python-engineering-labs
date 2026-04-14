# Mutation Testing

Estimated time: 2 hours

## Definition

Use mutations to measure whether tests truly protect behavior or only execute code paths superficially.

## What You Practice

- Mutants
- Killed vs survived
- Assertion strength
- Test design feedback

## Practical Applications

- Pricing engines
- classification rules
- decision trees

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply mutation testing in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement pricing rules where small operator changes should be caught by tests.

Success criteria:
- Implement `apply_tax`.
- Implement `apply_discount`.
- Implement `final_price`.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

