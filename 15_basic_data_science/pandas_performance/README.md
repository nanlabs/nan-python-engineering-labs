# Pandas Performance

Estimated time: 2-3 hours

## 1. Definition

Pandas Performance shows when to vectorize transformations, measure runtimes, and avoid unnecessary apply calls.

### Key Characteristics

- Compares strategies with simple, repeatable metrics.
- Favours columnar operations over row-by-row loops.
- Helps detect bottlenecks early.
- Pairs well with deeper profiling when needed.

## 2. Practical Application

### Use Cases

1. Speeding up discount or revenue calculation pipelines.
2. Reducing preprocessing time before model training.
3. Making informed decisions about when to migrate to Polars.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on pandas performance.

## 3. Why Is It Important?

### Problem It Solves

Without measuring and vectorizing, an apparently correct pipeline can degrade badly as data volume grows.

### Solution and Benefits

- Lets you justify changes with evidence instead of intuition.
- Reduces wasted CPU on repetitive operations.
- Improves the scalability of common transformations.

### Common Pitfalls

- Measuring only once and drawing final conclusions.
- Optimizing before validating correctness.
- Ignoring the cost of conversions between types or data structures.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Implement a vectorized discount strategy and compare it with a slower alternative.

### Basic Level

- Implement the core functionality requested in the exercise.
- Cover the nominal case with tests.

### Intermediate Level

- Validate invalid inputs or relevant edge cases.
- Refactor names and intermediate steps for clarity.

### Advanced Level

- Add a reusable variant or an extra validation useful in production.
- Document the key technical decision behind your solution.

### Success Criteria

- The solution produces the expected result for representative data.
- `tests/test_basic.py` communicates the minimum contract to preserve.
- The final code is clear enough for peer review.

## 6. Summary

- Performance improves when the transformation is expressed column by column.
- Measuring small changes avoids imaginary optimizations.
- Vectorization is not everything, but it is often the right first step.

## 7. Reflection Prompt

- Which part of the pipeline deserves deeper measurement?
- Which optimization keeps readability intact?
- When should you change tools instead of micro-optimizing?
