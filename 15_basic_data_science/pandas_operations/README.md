# Pandas Operations

Estimated time: 2-3 hours

## 1. Definition

Pandas Operations focuses on merges, groupby workflows, column transformations, and business-oriented summaries.

### Key Characteristics

- Combines datasets with explicit joins.
- Groups metrics by segment, category, or time period.
- Allows new derived columns in compact pipelines.
- Keeps intermediate aggregations visible for debugging.

## 2. Practical Application

### Use Cases

1. Joining orders with customers to segment revenue.
1. Aggregating metrics by product category.
1. Building summary tables before visualizing results.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on pandas operations.

## 3. Why Is It Important?

### Problem It Solves

When tabular transformations grow without structure, merges become opaque and repeated aggregations are hard to verify.

### Solution and Benefits

- Separates each transformation step into auditable pieces.
- Makes it easier to compare revenue, average ticket, and volume.
- Prepares data better for visualization or modeling.

### Common Pitfalls

- Joining tables without validating cardinality.
- Losing key columns after rename or reset_index.
- Hiding too much logic inside a single long chain.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Summarize revenue and average order value per segment by joining orders and customers.

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

- Tabular operations become clearer when each step has a purpose.
- Joins and groupby are the backbone of many business reports.
- Derived metrics should stay explicit and easy to verify.

## 7. Reflection Prompt

- Which cardinality assumptions did you need to validate?
- Which derived metric adds more context than the raw total?
- What would you change to make this pipeline reusable?
