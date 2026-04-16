# Alembic Migrations

Estimated time: 2 hours

## 1. Definition

**Alembic** is the database migration tool for SQLAlchemy. It tracks schema changes over time as versioned migration files, applies them in order, and supports rolling back to any previous revision.

### Key Characteristics

- **Revision files**: Python files with `upgrade()` and `downgrade()` functions.
- **`--autogenerate`**: compares SQLAlchemy models to the live schema and generates the diff automatically.
- **Linear history**: revisions form a linked list; each knows its predecessor (`revises`).
- **`alembic_version` table**: single-row table storing the current revision in the database.
- **`op` module**: `op.create_table`, `op.add_column`, `op.alter_column`, `op.execute`.

## 2. Practical Application

### Use Cases

- Initial schema creation on first deployment.
- Adding a column (`bio TEXT`) to an existing users table without data loss.
- Renaming columns with a two-phase migration (add new, migrate data, drop old).
- Rolling back a bad migration in staging before it reaches production.

### Code Example

```python
# alembic/versions/001_add_users.py

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(200), unique=True, nullable=False),
    )

def downgrade():
    op.drop_table("users")
```

## 3. Why Is It Important?

### Problem It Solves

Running `Base.metadata.create_all()` on a live database with existing data silently skips existing tables — it cannot add columns or modify constraints. Schema evolution requires migrations.

### Solution and Benefits

Alembic applies changes incrementally and reversibly. Every schema change has an audit trail. Staging and production stay in sync. Rollback is one command: `alembic downgrade -1`.

## 4. References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Initialize Alembic (`alembic init alembic`). Configure `env.py` with your `Base.metadata`. Generate an initial migration with `--autogenerate`. Apply it with `alembic upgrade head`.

### Intermediate Level

Add a `bio TEXT` column to the `users` table. Generate a new migration and apply it. Verify `alembic current` shows the new revision.

### Advanced Level

Write a data migration: in `upgrade()`, after adding the column, run `op.execute(text("UPDATE users SET bio = 'No bio' WHERE bio IS NULL"))`. Write the corresponding `downgrade()`.

### Success Criteria

- `alembic upgrade head` creates the schema from zero.
- `alembic downgrade base` removes everything.
- `alembic history` shows all revisions in order.
- Data migration preserves existing rows.

## 6. Summary

Alembic manages schema evolution as versioned, reversible migrations. `--autogenerate` compares models to the live schema and generates the diff. Every change is tracked in `alembic_version`. The `upgrade`/`downgrade` pair is the unit of schema change.

## 7. Reflection Prompt

What is the risk of using `--autogenerate` without reviewing the generated migration? What kinds of changes might Alembic miss or misrepresent, and how would you test a migration before applying it to production?
