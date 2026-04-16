"""
Tests for FastAPI Intro

Run with: pytest tests/test_basic.py -v
"""

import pytest
from pathlib import Path
import sys

parent_dir = Path(__file__).parent.parent / "my_solution"
sys.path.insert(0, str(parent_dir))


class TestFastapiIntro:
    """Test suite for FastAPI intro."""

    def test_basic_functionality(self):
        """Basic functionality test."""
        # TODO: Use TestClient to call GET / and assert 200 + message.
        pass

    def test_edge_cases(self):
        """Edge case test."""
        # TODO: Test GET /items/{id} with a non-existent ID and assert 404.
        pass

    def test_error_handling(self):
        """Error handling test."""
        # TODO: POST /items with invalid price (<= 0) and assert 422.
        pass


def test_imports():
    """Verify that imports work."""
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
