# Matplotlib Basics

Estimated time: 1.5-2.5 hours

## 1. Definition

Matplotlib Basics covers core plotting with explicit control over figures, axes, labels, and formatting.

### Key Characteristics

- Uses an object-oriented API for building plots.
- Works well as the foundation for more expressive plotting libraries.
- Can export figures without depending on a GUI backend.
- Is ideal for understanding what happens on each axis.

## 2. Practical Application

### Use Cases

1. Plotting monthly sales or traffic trends.
2. Annotating outliers or milestones in a time series.
3. Exporting charts for automated reporting.

### Code Example

Review `examples/example_basic.py` for an executable implementation focused on matplotlib basics.

## 3. Why Is It Important?

### Problem It Solves

If you do not control the figure and axes explicitly, plots become harder to reuse, test, or export consistently.

### Solution and Benefits

- Makes visualizations reproducible in scripts and pipelines.
- Lets you compose multiple series with clear labeling.
- Makes it easy to save outputs for QA or documentation.

### Common Pitfalls

- Relying on pyplot global state without closing figures.
- Skipping titles or labels and losing context.
- Adding too much decoration before validating the data story.

## 4. References

See `references/links.md` for official documentation and deeper material.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point. The exercise focuses on: Build a reusable figure with a monthly sales line and clear labels.

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

- Matplotlib helps you control every chart layer.
- Its object-oriented API improves testability and reuse.
- Saving figures without a UI is key for automation.

## 7. Reflection Prompt

- Which part of the chart should become a reusable function?
- Which label adds the most context for the reader?
- How would you validate that the figure stays correct after a refactor?
