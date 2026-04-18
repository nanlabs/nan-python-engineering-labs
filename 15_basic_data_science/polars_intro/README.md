# Polars Intro

Estimated time: 1.5-2.5 hours

## 1. Definition

Polars Intro introduces a modern columnar engine for fast analysis with explicit expressions and lazy evaluation.

### Key Characteristics

- Uses declarative expressions instead of implicit operations.
- Leverages columnar execution and internal parallelism.
- Supports eager and lazy modes depending on the workload.
- Acts as a modern alternative for some Pandas pipelines.

## 2. Practical Application

### Use Cases

1. Grouping larger datasets with readable expressions.
2. Migrating slow parts of an exploratory pipeline.
3. Comparing ergonomics and performance against Pandas.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on polars intro.

## 3. Why Is It Important?

### Problem It Solves

As a pipeline grows, some tabular transformations benefit from a more explicit API and a better-optimized execution model.

### Solution and Benefits

- Makes per-column expressions more visible.
- Often performs very well on large aggregations and filters.
- Encourages thinking about the pipeline as a declarative sequence.

### Common Pitfalls

- Translating Pandas patterns 1:1 and missing expression-based advantages.
- Ignoring the difference between eager and lazy execution.
- Failing to validate the expected schema after transformations.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Summarize shipments by warehouse with declarative Polars aggregations.

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

- Polars changes how you think about tabular transformations.
- Explicit expressions help you reason about the pipeline.
- It is useful when Pandas starts falling short for specific workflows.

## 7. Reflection Prompt

- Which part of the pipeline becomes clearer with expressions?
- What criteria would you use to choose between Pandas and Polars?
- Which schema would you validate at the end?
