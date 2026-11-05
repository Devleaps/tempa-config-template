---
description: "Working with Postgres: stores, migrations and the traps to avoid"
---

# Postgres

## Stores

- One store per feature: a pool or session injected, a `row_to_x` / `rowToX` mapper to the domain type in
  camelCase or snake_case as the language prefers.
- Node's `pg` driver returns `bigint`, `BIGSERIAL` and `NUMERIC` as **strings**: convert with `Number(...)`
  in the mapper, and prove it with a real-Postgres test (an in-memory twin cannot catch it).
- `JSONB` comes back parsed; write it with `JSON.stringify(...)` and a `::jsonb` cast (Node) or the dialect's
  JSON type (SQLAlchemy).
- Keep `bytea` and other large columns out of list and detail queries; select `(col IS NOT NULL) AS has_x`.
- Parameterised queries only. Dynamic updates go through a small helper that adds `col = $n` per supplied
  field.
- Dedupe with partial unique indexes over live rows (`WHERE cleared_at IS NULL`), and serialise concurrent
  writers with an advisory lock when a check-then-insert cannot be a single statement.

## Migrations

- Every schema change is a migration (Alembic in Python, numbered SQL files in Node). Never edit one that
  has shipped; never change the baseline.
- Migrations are idempotent and re-runnable (`IF NOT EXISTS`; guard `ADD CONSTRAINT` with a `DO $$ ... $$`
  check on `pg_constraint`).
- Check open branches before taking a migration number: reusing a number another branch took is the real
  hazard; gaps are harmless.
- Changing a `CHECK`ed enum: drop the old constraint before the `UPDATE` that rewrites values, then add the
  new one.
- Verify a data-rewriting migration against seeded fixture data; an empty local table proves nothing.
- Destructive changes (drop a column or table) come in two releases: stop reading it, then drop it.

## Operations

- Managed Postgres over TLS; the connection string comes from the secret store.
- Tables that must be tamper-evident (audit logs) are append-only at the database level: no update or
  delete grants for the app role, enforced by triggers as well.
- `pg_dump -Fc` before any manual data operation, and never run one against production without a second
  person.
