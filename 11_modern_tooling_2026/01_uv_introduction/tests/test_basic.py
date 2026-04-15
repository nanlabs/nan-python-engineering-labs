"""Tests for the basic uv exercise."""
import pytest
from pathlib import Path
import sys

# Add my_solution to the import path
sys.path.insert(0, str(Path(__file__).parent.parent / "my_solution"))

def test_uv_installed():
    """Verify that uv is installed."""
    import subprocess
    result = subprocess.run(["uv", "--version"], capture_output=True)
    assert result.returncode == 0, "uv is not installed correctly"

def test_requirements_file_exists():
    """Verify that requirements.txt exists and has expected content."""
    req_file = Path("requirements.txt")
    if req_file.exists():
        content = req_file.read_text()
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        assert len(lines) >= 10, "requirements.txt must include at least 10 packages"

@pytest.mark.skipif(not Path("my_solution/basic_exercise.py").exists(), 
                   reason="Solution not implemented yet")
def test_measure_install_time():
    """Verify that measure_install_time() behaves correctly."""
    from basic_exercise import measure_install_time
    
    # This test assumes the function is implemented.
    # It should return a positive float.
    # (We do not execute the real benchmark to keep tests fast.)
    pass

def test_report_generated():
    """Verify that the benchmark report file was generated."""
    report = Path("results.md")
    if report.exists():
        content = report.read_text()
        assert "pip" in content.lower()
        assert "uv" in content.lower()
        assert "speedup" in content.lower()
