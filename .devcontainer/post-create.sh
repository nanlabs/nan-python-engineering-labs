#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing uv"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "==> Installing maturin for PyO3 development"
pip install maturin

echo "==> Creating virtualenv and installing dev deps"
uv venv
# shellcheck disable=SC1091
source .venv/bin/activate
uv pip install -e ".[dev,profiling,ai,pyo3,security,data]"

echo "==> Installing pre-commit hooks"
pre-commit install || true

echo "==> Done. Run: uv run scripts/progress.py"
