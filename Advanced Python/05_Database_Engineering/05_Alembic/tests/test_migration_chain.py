from __future__ import annotations

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations"


def _script_directory() -> ScriptDirectory:
    cfg = Config()
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    return ScriptDirectory.from_config(cfg)


def test_migration_chain_has_single_head() -> None:
    script = _script_directory()
    heads = script.get_heads()
    assert len(heads) == 1


def test_migration_chain_is_linear_and_reaches_initial_revision() -> None:
    script = _script_directory()
    head = script.get_current_head()
    revisions = list(script.walk_revisions(base="base", head=head))
    revision_ids = [rev.revision for rev in revisions]
    assert "0001" in revision_ids
    assert "0003" in revision_ids
    assert len(revision_ids) == len(set(revision_ids))


def test_every_migration_defines_upgrade_and_downgrade() -> None:
    script = _script_directory()
    for revision in script.walk_revisions():
        module = revision.module
        assert hasattr(module, "upgrade")
        assert hasattr(module, "downgrade")
