# NumPy Basics

Estimated time: 1.5-2.5 hours

## 1. Definition

NumPy Basics introduces multidimensional arrays, broadcasting, and vectorized operations for numeric workloads without explicit Python loops.

### Key Characteristics

- Works with homogeneous arrays and contiguous memory layouts.
- Uses vectorized operations for clearer and faster numeric code.
- Relies on broadcasting to combine series of different shapes.
- Acts as a foundation for much of the Python scientific stack.

## 2. Practical Application

### Use Cases

1. Normalizing metrics before training a simple model.
1. Computing daily KPIs from sales or traffic series.
1. Preparing numerical features for exploratory analysis.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on numpy basics.

## 3. Why Is It Important?

### Problem It Solves

Without vectorized arrays, numeric code scales poorly, becomes verbose, and mixes business logic with low-level iteration details.

### Solution and Benefits

- Reduces the cost of processing large numeric lists.
- Makes mathematical transformations easier to read.
- Acts as a bridge to Pandas, SciPy, and machine learning tools.

### Common Pitfalls

- Confusing element-wise operations with matrix multiplication.
- Ignoring dtypes and silently losing numeric precision.
- Overusing unnecessary conversions between lists and arrays.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Implement a reusable z-score normalization and moving average for a numeric series.

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

- NumPy lets you work with numeric data at a column or vector level.
- Vectorized operations simplify repeated calculations.
- It is the natural starting point for data science in Python.

## 7. Reflection Prompt

- Which part of the calculation became clearer when expressed with arrays?
- Where did you gain readability compared to a list-based solution?
- What validations would you add before reusing this logic?
