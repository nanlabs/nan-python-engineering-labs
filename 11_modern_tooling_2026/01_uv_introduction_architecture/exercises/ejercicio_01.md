# Exercise 1: Exploring uv

## Objective
Become familiar with uv basic commands and understand its architecture.

## Instructions

### Part 1: Installation and Verification (10 min)

1. Check whether uv is installed:
   ```bash
   uv version
   ```

2. If it is not installed, install it:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Check the cache location:
   ```bash
   uv cache dir
   ```

4. Explore cache contents (if present):
   ```bash
   ls -lh $(uv cache dir)
   ```

### Part 2: Speed Comparison (15 min)

5. Create two test directories:
   ```bash
   mkdir -p /tmp/test-pip /tmp/test-uv
   ```

6. Using traditional pip:
   ```bash
   cd /tmp/test-pip
   time python3 -m venv .venv
   time .venv/bin/pip install requests beautifulsoup4 pandas
   ```

7. Using uv:
   ```bash
   cd /tmp/test-uv
   time uv venv
   time uv pip install requests beautifulsoup4 pandas
   ```

8. Compare timings. How much faster is uv?

### Part 3: Understanding Cache Behavior (15 min)

9. Install the same package in two different projects with uv:
   ```bash
   mkdir -p /tmp/project-a /tmp/project-b
   cd /tmp/project-a && uv venv && uv pip install flask==3.0.0
   cd /tmp/project-b && uv venv && uv pip install flask==3.0.0
   ```

10. Check the output of the second installation. Was it instant?

11. Check cache size:
    ```bash
    du -sh $(uv cache dir)
    ```

### Part 4: Research (20 min)

12. Read about the PubGrub algorithm:
    - Visita: https://github.com/dart-lang/pub/blob/master/doc/solver.md
    - Summarize in 3 points how it differs from backtracking

13. Experiment with dependency conflicts:
    ```bash
    mkdir /tmp/conflict-test && cd /tmp/conflict-test
    uv venv
    # Try to install incompatible versions
    uv pip install "requests==2.25.0" "urllib3==2.0.0"
    ```

14. Compare uv vs pip error messages. Which one is clearer?

## Reflection Questions

1. Why is uv faster than pip?
2. What benefits does the global cache provide?
3. In which scenarios is uv most beneficial?
4. What drawbacks or risks can you identify?

## Deliverables

Create a file named `RESPUESTAS.md` in `my_solution/` including:
- Timing captures from comparisons
- Answers to reflection questions
- A 3-5 line summary about PubGrub

## Success Criteria

- ✅ uv installed and working
- ✅ Speed comparison executed and documented
- ✅ Understanding of global cache behavior
- ✅ Basic understanding of PubGrub
