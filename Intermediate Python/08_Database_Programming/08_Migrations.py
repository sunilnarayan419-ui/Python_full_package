"""
08_Migrations.py

Demonstrates the production schema-migration lifecycle for the
scientific data platform using Alembic + SQLAlchemy:

    Model change -> Migration generation -> Migration review ->
    Migration execution -> Schema version tracking

This module does NOT modify a real/production database and does NOT run
destructive migrations on import or on normal execution. It builds a
throwaway Alembic environment against a temporary SQLite database purely
to demonstrate the mechanics of revision scripts, upgrade()/downgrade(),
and version tracking. If Alembic is not installed, it fails gracefully
with a clear diagnostic.

Realistic schema evolution modeled here:

    Version 1: samples(id, species)
    Version 2: samples(id, species, collection_location)
    Version 3: measurements(id, sample_id -> samples.id, metric_name, metric_value)

Each revision is:
  - deterministic (fixed revision id, fixed down_revision chain)
  - reviewable (plain Python, checked into version control in a real repo)
  - reversible where realistically possible (downgrade() provided for
    each additive change)
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from textwrap import dedent

logger = logging.getLogger(__name__)

try:
    import alembic  # noqa: F401
    from alembic import command
    from alembic.config import Config
    _ALEMBIC_AVAILABLE = True
except ImportError:  # pragma: no cover - environment dependent
    _ALEMBIC_AVAILABLE = False


class MigrationsUnavailableError(RuntimeError):
    """Raised when Alembic is not installed."""


# ---------------------------------------------------------------------------
# The three revision scripts below are written out as files inside a
# temporary "migrations/versions" directory for the demo. In a real
# project these would be permanent, version-controlled files generated
# via `alembic revision --autogenerate -m "..."` and then hand-reviewed
# before being committed -- autogeneration is a starting draft, not a
# substitute for review.
# ---------------------------------------------------------------------------

_REVISION_1 = dedent(
    '''
    """create samples table (v1: id, species)"""
    from alembic import op
    import sqlalchemy as sa

    revision = "0001_create_samples"
    down_revision = None
    branch_labels = None
    depends_on = None


    def upgrade() -> None:
        op.create_table(
            "samples",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("species", sa.String(120), nullable=False),
        )


    def downgrade() -> None:
        op.drop_table("samples")
    '''
).strip()

_REVISION_2 = dedent(
    '''
    """add collection_location to samples (v2)"""
    from alembic import op
    import sqlalchemy as sa

    revision = "0002_add_collection_location"
    down_revision = "0001_create_samples"
    branch_labels = None
    depends_on = None


    def upgrade() -> None:
        # Additive, backward-compatible change: existing rows get NULL
        # for the new column rather than requiring a default backfill
        # that could lock a large production table.
        op.add_column("samples", sa.Column("collection_location", sa.String(200), nullable=True))


    def downgrade() -> None:
        op.drop_column("samples", "collection_location")
    '''
).strip()

_REVISION_3 = dedent(
    '''
    """add measurements table with FK to samples (v3)"""
    from alembic import op
    import sqlalchemy as sa

    revision = "0003_add_measurements"
    down_revision = "0002_add_collection_location"
    branch_labels = None
    depends_on = None


    def upgrade() -> None:
        op.create_table(
            "measurements",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("sample_id", sa.Integer, sa.ForeignKey("samples.id"), nullable=False),
            sa.Column("metric_name", sa.String(80), nullable=False),
            sa.Column("metric_value", sa.Float, nullable=False),
        )
        op.create_index(
            "idx_measurements_sample_id", "measurements", ["sample_id"]
        )


    def downgrade() -> None:
        op.drop_index("idx_measurements_sample_id", table_name="measurements")
        op.drop_table("measurements")
    '''
).strip()


def _write_migration_environment(root: Path, db_path: Path) -> Path:
    """
    Assembles a minimal, self-contained Alembic environment (alembic.ini +
    env.py + versions/*.py) inside a temporary directory. This mirrors the
    structure `alembic init` produces, trimmed to what's needed for a
    non-interactive demo.
    """
    versions_dir = root / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)

    (versions_dir / "0001_create_samples.py").write_text(_REVISION_1)
    (versions_dir / "0002_add_collection_location.py").write_text(_REVISION_2)
    (versions_dir / "0003_add_measurements.py").write_text(_REVISION_3)

    env_py = dedent(
        f"""
        from alembic import context
        from sqlalchemy import engine_from_config, pool

        config = context.config

        def run_migrations_offline():
            context.configure(
                url=config.get_main_option("sqlalchemy.url"),
                literal_binds=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        def run_migrations_online():
            connectable = engine_from_config(
                config.get_section(config.config_ini_section, {{}}),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )
            with connectable.connect() as connection:
                context.configure(connection=connection)
                with context.begin_transaction():
                    context.run_migrations()

        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()
        """
    ).strip()
    (root / "env.py").write_text(env_py)

    alembic_ini = root / "alembic.ini"
    alembic_ini.write_text(
        dedent(
            f"""
            [alembic]
            script_location = {root}
            sqlalchemy.url = sqlite:///{db_path}
            """
        ).strip()
    )
    return alembic_ini


def run_migration_demo() -> None:
    if not _ALEMBIC_AVAILABLE:
        raise MigrationsUnavailableError(
            "alembic is not installed. Install it with `pip install alembic` "
            "to run schema migrations."
        )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        db_path = tmp_path / "migration_demo.db"
        migrations_root = tmp_path / "migrations"

        ini_path = _write_migration_environment(migrations_root, db_path)
        cfg = Config(str(ini_path))

        # upgrade() lifecycle: apply revisions in order, tracked via
        # Alembic's alembic_version table inside the target database --
        # this is how the schema's current version is recorded and how
        # Alembic knows which migrations still need to run next time.
        logger.info("applying migrations up to head (v1 -> v2 -> v3)")
        command.upgrade(cfg, "head")
        print("upgraded schema to head revision (0003_add_measurements)")

        # Demonstrate that downgrade() is available and reviewed, without
        # actually leaving the demo database in a downgraded state
        # unexpectedly -- we downgrade one step and immediately
        # re-upgrade, mirroring how a team would test rollback safety in
        # a staging environment before trusting it in production.
        logger.info("demonstrating a reviewed rollback of the latest revision")
        command.downgrade(cfg, "-1")
        command.upgrade(cfg, "head")
        print("demonstrated downgrade(-1) followed by re-upgrade(head)")

        current = command.current(cfg, verbose=False)
        print(f"migration demo complete; alembic tracks current revision internally "
              f"(command.current output shown above if verbose logging is enabled)")


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)
    try:
        run_migration_demo()
    except MigrationsUnavailableError as exc:
        print(f"migrations demo skipped: {exc}")

    print(
        "reminder: autogenerated migrations must always be reviewed by a "
        "human before being committed or run against a production "
        "database; this module never touches production infrastructure."
    )


if __name__ == "__main__":
    _run_demo()
