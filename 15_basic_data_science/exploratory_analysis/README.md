# Exploratory Analysis

Estimated time: 2-3 hours

## 1. Definition

Exploratory Analysis organizes the first pass through a dataset to detect patterns, outliers, and new questions.

### Key Characteristics

- Summarizes numeric and categorical variables quickly.
- Looks for anomalies before deeper modeling work.
- Connects descriptive metrics with business hypotheses.
- Produces clear inputs for later charts and decisions.

## 2. Practical Application

### Use Cases

1. Reviewing sales behavior by region and channel.
2. Detecting unusual ranges before training a model.
3. Prioritizing questions for downstream visualization.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on exploratory analysis.

## 3. Why Is It Important?

### Problem It Solves

Without early exploration, it is easy to build dashboards or models on top of wrong assumptions and hidden biases.

### Solution and Benefits

- Helps you formulate better questions before automating anything.
- Makes outliers, skew, and information gaps visible.
- Reduces the cost of fixing late-stage decisions.

### Common Pitfalls

- Confusing description with causality.
- Falling in love with a single summary metric.
- Failing to separate observed findings from final conclusions.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Build a compact EDA report with numeric summaries and a dominant category.

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

- EDA guides what to inspect before going deeper.
- The value comes from combining numbers, context, and questions.
- A small, well-built report can unlock many next steps.

## 7. Reflection Prompt

- Which finding would change a business decision?
- Which metric turned out to be less informative than expected?
- Which chart would you build after this report?
