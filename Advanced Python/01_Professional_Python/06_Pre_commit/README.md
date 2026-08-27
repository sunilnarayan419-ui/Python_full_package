# 06_Pre_commit

Realistic `.pre-commit-config.yaml` wiring together hygiene hooks
(trailing whitespace, large-file/merge-conflict checks, secret
detection), Ruff (lint + format), strict mypy, and Bandit security
linting. `release_gate/` is a small, dependency-free module a local
pre-push hook could invoke directly.

Run: `pre-commit run --all-files`
