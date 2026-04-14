# Parametrize

Estimated time: 2 hours

## Definition

Cover many inputs with a compact test matrix instead of repeating the same assertions by hand.

## What You Practice

- Parametrize decorator
- Input matrices
- Ids
- Negative cases

## Practical Applications

- Validation rules
- Formatting logic
- Business policy tables

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply parametrize in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement normalization and validation helpers that benefit from a dense input matrix.

Success criteria:
- Implement `normalize_email`.
- Implement `is_company_email`.
- Implement `extract_domain`.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

