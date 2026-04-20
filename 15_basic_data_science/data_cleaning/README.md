# Data Cleaning

Estimated time: 2-3 hours

## 1. Definition

Data Cleaning focuses on standardizing columns, handling missing values, and removing inconsistencies before analysis.

### Key Characteristics

- Improves data quality before modeling or visualization.
- Turns cleaning rules into repeatable steps.
- Makes assumptions about missing values and duplicates explicit.
- Reduces noise in later metrics and dashboards.

## 2. Practical Application

### Use Cases

1. Normalizing names and columns when importing varied CSV files.
1. Filling missing revenue with a simple, documented strategy.
1. Removing duplicates before calculating totals.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on data cleaning.

## 3. Why Is It Important?

### Problem It Solves

If cleaning stays implicit or manual, downstream analysis becomes unreliable and hard to reproduce.

### Solution and Benefits

- Improves confidence in each downstream pipeline step.
- Makes missing-data decisions auditable.
- Reduces silent errors in joins and aggregations.

### Common Pitfalls

- Filling missing values without explaining the rule.
- Dropping rows without measuring the impact on total volume.
- Failing to record which columns were renamed or transformed.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Standardize a customer dataset by fixing column names, missing values, and duplicates.

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

- Cleaning is an explicit stage, not a minor detail.
- Repeatable rules improve reliability and maintenance.
- A clean dataset prevents downstream analysis errors.

## 7. Reflection Prompt

- Which transformation had the biggest impact on final data quality?
- Which imputation decision deserves clearer documentation?
- How would you compare the dataset before and after cleaning?
