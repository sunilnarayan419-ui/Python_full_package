# 08_Config_Management

Immutable, typed application settings with explicit precedence
(overrides > environment variables > `.env` file > defaults),
environment-aware validation (e.g. rejects `debug=True` in
`production`), and no hardcoded secrets — `.env.example` documents
required variables without real values.

Run: `pytest tests/`
