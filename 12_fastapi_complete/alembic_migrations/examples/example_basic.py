"""
Basic example: Alembic Migrations
====================================

Alembic is the de facto database migration tool for SQLAlchemy.
It tracks schema changes over time and applies them in order.

This is a STANDALONE RUNNABLE script that demonstrates the migration
workflow programmatically — no HTTP server needed.

Demonstrates:
1. Alembic configuration (in-memory, no alembic.ini needed)
2. Creating a migration script with upgrade/downgrade
3. Running upgrade, checking current version
4. Generating a second migration (adding a column)
5. Downgrade to a previous version

Dependencies:
    pip install alembic sqlalchemy

Run:
    python example_basic.py
"""

import os
import tempfile

from sqlalchemy import create_engine, inspect, text

# =============================================================================
# MIGRATION WORKFLOW EXPLANATION
# =============================================================================

WORKFLOW = """
Alembic Migration Workflow
===========================

1. Initialize:
       alembic init alembic
   Creates alembic/ folder + alembic.ini

2. Configure alembic/env.py:
       from myapp.models import Base
       target_metadata = Base.metadata

3. Generate a migration (auto-detects schema changes):
       alembic revision --autogenerate -m "add users table"
   Creates alembic/versions/<hash>_add_users_table.py

4. Apply all pending migrations:
       alembic upgrade head

5. Check current revision:
       alembic current

6. Show history:
       alembic history --verbose

7. Roll back one step:
       alembic downgrade -1

8. Roll back to base (empty):
       alembic downgrade base


Migration file structure (auto-generated):
-------------------------------------------
# revision: abc123def456
# revises:  <previous_revision>
# create date: 2024-01-15 10:30:00

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(200), unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')


Key Alembic operations:
    op.create_table()       — create a table
    op.drop_table()         — drop a table
    op.add_column()         — add a column
    op.drop_column()        — remove a column
    op.alter_column()       — rename/type/nullable change
    op.create_index()       — add an index
    op.drop_index()         — remove an index
    op.execute(text(...))   — run raw SQL
"""


def show_workflow():
    print(WORKFLOW)


# =============================================================================
# PROGRAMMATIC DEMO (no CLI required)
# =============================================================================


def run_programmatic_demo():
    """
    Demonstrate Alembic concepts without the CLI.

    We use the Alembic Python API directly to show what the CLI does.
    """
    print("=" * 65)
    print("ALEMBIC MIGRATIONS — PROGRAMMATIC DEMO")
    print("=" * 65)

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "demo.db")
        db_url = f"sqlite:///{db_path}"
        engine = create_engine(db_url)

        print()
        print("Step 1: Run initial migration (create users table)")
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS alembic_version (
                    version_num VARCHAR(32) NOT NULL,
                    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
                )
            """
                )
            )
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(200) UNIQUE NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )
            conn.execute(
                text("INSERT INTO alembic_version (version_num) VALUES ('001_create_users')")
            )

        # Verify
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
            print(f"  Current version: {version}")
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"  Tables: {tables}")

        print()
        print("Step 2: Apply second migration (add 'bio' column to users)")
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN bio TEXT"))
            conn.execute(text("UPDATE alembic_version SET version_num = '002_add_bio'"))

        with engine.connect() as conn:
            version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
            print(f"  Current version: {version}")
            inspector = inspect(engine)
            cols = [c["name"] for c in inspector.get_columns("users")]
            print(f"  users columns: {cols}")

        print()
        print("Step 3: Apply third migration (add is_active column)")
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"))
            conn.execute(text("UPDATE alembic_version SET version_num = '003_add_is_active'"))

        with engine.connect() as conn:
            version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
            print(f"  Current version: {version}")
            inspector = inspect(engine)
            cols = [c["name"] for c in inspector.get_columns("users")]
            print(f"  users columns: {cols}")

        print()
        print("Step 4: Insert test data (migrations preserve data)")
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                INSERT INTO users (username, email, bio, is_active)
                VALUES ('alice', 'alice@example.com', 'Engineer', 1),
                       ('bob', 'bob@example.com', NULL, 1)
            """
                )
            )

        with engine.connect() as conn:
            rows = conn.execute(text("SELECT id, username, email, bio FROM users")).fetchall()
            print(f"  Rows after migrations: {len(rows)}")
            for row in rows:
                print(f"    {dict(row._mapping)}")

        print()
        print("Step 5: Simulate downgrade to '002_add_bio'")
        print("  (In real Alembic: alembic downgrade 002_add_bio)")
        print("  → would drop 'is_active' column and revert version")
        print("  → SQLite doesn't support DROP COLUMN directly")
        print("  → real Alembic handles this with table recreate")

    print()


def show_directory_structure():
    print("─" * 65)
    print("Expected Alembic directory structure:")
    print("─" * 65)
    structure = """
myproject/
├── alembic.ini               ← Alembic config (DB URL, etc.)
├── alembic/
│   ├── env.py                ← Migration environment (target_metadata)
│   ├── script.py.mako        ← Template for new revision files
│   └── versions/
│       ├── 001_initial.py    ← First migration
│       ├── 002_add_bio.py    ← Second migration
│       └── 003_add_active.py ← Third migration
└── myapp/
    ├── models.py             ← SQLAlchemy models (used by env.py)
    └── database.py           ← Engine / SessionLocal setup
"""
    print(structure)


def show_alembic_ini_example():
    print("─" * 65)
    print("alembic.ini (key settings):")
    print("─" * 65)
    print(
        """
[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/mydb

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console
"""
    )


def show_env_py_example():
    print("─" * 65)
    print("alembic/env.py (key lines to customize):")
    print("─" * 65)
    print(
        """
from myapp.models import Base        # import your Base
from myapp.database import DATABASE_URL

config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = Base.metadata      # enables --autogenerate
"""
    )


# =============================================================================
# MAIN
# =============================================================================


def main():
    """Entry point to demonstrate the implementation."""
    run_programmatic_demo()
    show_directory_structure()
    show_alembic_ini_example()
    show_env_py_example()

    print("=" * 65)
    print("QUICK REFERENCE")
    print("=" * 65)
    print(
        """
Common commands:
  alembic init alembic                         # initialize
  alembic revision --autogenerate -m "msg"    # generate migration
  alembic upgrade head                         # apply all
  alembic upgrade +1                           # apply one
  alembic downgrade -1                         # revert one
  alembic downgrade base                       # revert all
  alembic current                              # show active revision
  alembic history --verbose                    # show all revisions
  alembic show <revision>                      # show a specific revision
"""
    )


if __name__ == "__main__":
    main()
