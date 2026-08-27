# 05_isort

Multi-module RNA-seq ingestion package demonstrating realistic import
separation: stdlib, third-party (numpy/pandas), first-party
(`data_ingest.*`), and local-folder imports, enforced via
`[tool.isort]` with the `black` profile.

Run: `isort --check-only src tests` and `pytest tests/`
