# Coverage Analysis

Estimated time: 2 hours

## Definition

Interpret coverage as a signal, not a vanity metric, and use missing lines to sharpen test suites.

## What You Practice

- Statement coverage
- Branch coverage
- Coverage reports
- Risk-based testing

## Practical Applications

- Critical pricing logic
- data validation code
- refactoring legacy modules

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply coverage analysis in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement pricing rules with edge cases that are easy to miss without coverage feedback.

Success criteria:
- Implement `loyalty_discount`.
- Implement `shipping_cost`.
- Implement `final_amount` that composes both.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

