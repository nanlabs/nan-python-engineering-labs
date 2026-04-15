"""
Basic Exercise: Compare pip vs uv on your machine

Objective: Install uv and measure the speedup on your system.

TODO:
1. Install uv:
    curl -LsSf https://astral.sh/uv/install.sh | sh

2. Create a requirements.txt file with 10 packages:
    - requests
    - pandas
    - numpy
    - pytest
    - flask
    - (add 5 more that you commonly use)

3. Implement measure_install_time() to:
    - Create a temporary virtual environment
    - Install packages
    - Measure total elapsed time
    - Clean up the virtual environment

4. Run the benchmark with pip and with uv (without cache)

5. Generate a report:
    - pip time: X seconds
    - uv time: Y seconds
    - Speedup: Z times
    - Conclusion

Success criteria:
- uv installed successfully (verify with: uv --version)
- Benchmark runs without errors
- Speedup > 5x
- Report written in results.md
"""

def measure_install_time(tool: str, requirements_file: str) -> float:
    """
    Measure package installation time.
    
    Args:
        tool: "pip" or "uv"
        requirements_file: Path to requirements.txt
    
    Returns:
        Time in seconds
    """
    # TODO: Implement
    pass

def generate_report(pip_time: float, uv_time: float) -> None:
    """
    Generate a markdown report with benchmark results.
    
    Args:
        pip_time: pip time in seconds
        uv_time: uv time in seconds
    """
    # TODO: Implement
    pass

if __name__ == "__main__":
    # TODO: Implement the main workflow
    print("Exercise: Benchmark pip vs uv")
    print("Complete the TODO functions above")
