# Pandas Intro

Estimated time: 1.5-2.5 hours

## 1. Definition

Pandas Intro shows how to represent tabular data with DataFrames and Series for basic filtering, aggregation, and reporting.

### Key Characteristics

- Works with labeled columns and mixed data types.
- Provides high-level filtering and aggregation APIs.
- Moves from JSON-like records to analysis tables quickly.
- Integrates naturally with CSV, Excel, and databases.

## 2. Practical Application

### Use Cases

1. Building simple sales dashboards from record lists.
2. Filtering orders by region or product line.
3. Creating monthly summaries for stakeholders.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on pandas intro.

## 3. Why Is It Important?

### Problem It Solves

Without an expressive tabular structure, cleaning and summarizing business data ends up scattered across lists, dicts, and hard-to-maintain loops.

### Solution and Benefits

- Makes the dataset shape visible from the start.
- Reduces the effort required to filter, group, and sort data.
- Helps move from exploration to basic reporting quickly.

### Common Pitfalls

- Building derived columns with inconsistent types.
- Forgetting to parse dates before grouping.
- Assuming the index has business meaning when it does not.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Build a sales DataFrame and calculate monthly revenue with core Pandas operations.

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

- Pandas organizes tabular data with a highly expressive model.
- Series and DataFrames cover most early-stage analysis needs.
- Clear columns and filters accelerate exploratory work.

## 7. Reflection Prompt

- Which derived column added the most analytical value?
- Where did groupby help more than a loop-based approach?
- What validation would you add before publishing this report?
