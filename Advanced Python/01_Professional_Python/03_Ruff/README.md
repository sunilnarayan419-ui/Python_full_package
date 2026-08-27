# 03_Ruff

Sequencing QC module written and configured to satisfy a strict Ruff rule
set (`pyproject.toml`): pycodestyle, pyflakes, isort, pep8-naming,
pyupgrade, bugbear, comprehensions, simplify, bandit-security, and a
pylint subset, with pytest-style per-file relaxations for tests.

Run: `ruff check src tests` and `ruff format --check src tests`
