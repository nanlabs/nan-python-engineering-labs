#!/bin/bash

# Install uv (ultra-fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Install maturin for PyO3 development
pip install maturin

# Create virtual environment with uv
uv venv

# Install project dependencies
uv pip install -e ".[dev,profiling,ai,pyo3,security]"

# Install pre-commit hooks
pre-commit install

# Verify installations
echo "✅ uv version: $(uv --version)"
echo "✅ ruff version: $(ruff --version)"
echo "✅ basedpyright version: $(basedpyright --version)"
echo "✅ pytest version: $(pytest --version)"
echo "✅ maturin version: $(maturin --version)"
echo ""
echo "🚀 DevContainer setup complete!"
echo "📚 Start learning with: uv run scripts/progress.py"
