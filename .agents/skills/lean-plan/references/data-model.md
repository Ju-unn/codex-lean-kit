# Data model checklist (SQLite via node:sqlite)

## Normalize (default: 3NF)
- **1NF**: atomic values.
  - No lists in a column (CSV, JSON arrays).
  - No repeating column groups (tag1, tag2).
- **2NF**: with a composite key, every column depends on the whole key, not part of it.
- **3NF**: no column depends on another non-key column (no transitive dependency). Example: orders stores customer_id, not customer_name.
- Derived values are computed, not stored: totals, counts, status computable from other rows.
- Denormalize only for a measured read cost, with the reason recorded in docs/plan.md Decisions.

## Types and naming
- Primary keys: `INTEGER PRIMARY KEY` (rowid alias), unless a natural key never changes.
- Money and counts: INTEGER in minor units. Never REAL for money.
- Times: ISO-8601 TEXT in UTC. Store a timestamp, not just a date, when order matters.
- Flags: INTEGER 0/1 with `CHECK (x IN (0,1))`. Enumerations: TEXT with `CHECK (status IN (...))`.
- Identifiers: lowercase_snake_case, plural table names, `<table>_id` for foreign keys.

## Constraints (the database enforces the rules, not only the code)
- Every table has a PRIMARY KEY.
- Every relationship has a FOREIGN KEY with a chosen ON DELETE:
  - RESTRICT by default.
  - CASCADE only for children the parent owns.
  - SET NULL only when the child stays meaningful without its parent.
- NOT NULL unless absence has a meaning.
- UNIQUE for natural identifiers (email, code), and for one-of rules ("one open request per item": a partial unique index).
- CHECK for value rules (qty > 0, end_at > start_at).
- History that must survive (orders, audit logs): never hard-delete. Use status columns or append-only tables.

## Indexes
- Index every foreign key used in joins or lookups.
- Index columns in frequent WHERE and ORDER BY. In a composite index, put the equality column first, then the range column.
- Use a partial index for "active only" lookups: `CREATE INDEX ... WHERE status = 'pending'`.
- Each index gets a one-line reason naming the query that needs it. No speculative indexes; each one slows writes.

## Queries and writes
- Statements are always parameterized: `db.prepare('SELECT ... WHERE id = ?').get(id)`. Never string-built SQL.
- Select the columns you need; avoid `SELECT *` in API responses.
- No query per item in a loop (N+1). Use a JOIN or `WHERE id IN (...)`.
- A change touching more than one row or table runs in one transaction: `BEGIN` ... `COMMIT`, `ROLLBACK` on error.
- Rules that concurrent requests can break are enforced in SQL. Covers stock, seats, balances, one-pending rules.
  - Tools: UNIQUE, CHECK, or a conditional `UPDATE ... WHERE qty >= ?` whose changed-row count is checked.
- Keep transactions short; never hold one across an await on something slow.

## SQLite specifics
- Run `PRAGMA foreign_keys = ON;` on every connection; it is off by default.
- schema.sql is idempotent (`CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`). It runs at startup, and on ':memory:' in tests.
- The DB file lives outside the repo or is git-ignored (`*.db`).

## Review questions
- Can one fact be updated in two places? Normalize.
- Which query needs each index?
- What happens to children when a parent is deleted?
- Which business rule would break if two requests arrived at once, and which constraint stops it?
- Which records must never be lost, and how is that enforced?

Sources: softaworks/agent-toolkit database-schema-designer (normalization, constraints, index checklist); affaan-m/ECC database-reviewer (types, FK indexing, N+1, short transactions; PostgreSQL items translated to SQLite).
