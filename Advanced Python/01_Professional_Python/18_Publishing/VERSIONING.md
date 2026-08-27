# Versioning strategy

`bioseqkit` follows Semantic Versioning (`MAJOR.MINOR.PATCH`):

- `MAJOR`: incompatible public-API changes (anything exported from
  `bioseqkit/__init__.py`).
- `MINOR`: backward-compatible functionality additions.
- `PATCH`: backward-compatible bug fixes only.

The single source of truth for the current version is
`src/bioseqkit/version.py::__version__`; `pyproject.toml`'s
`[project].version` must be bumped in the same commit. A release is
cut by tagging `vX.Y.Z` on `main` after CI (tests, mypy, ruff) is green
on that commit; the tag triggers the publish workflow, which runs
`scripts/build_and_validate.py` before any upload step.
