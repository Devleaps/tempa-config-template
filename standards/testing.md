---
description: "How to test: what to test, against what, and with which data"
---

# Testing

## What

- Every acceptance criterion has a test or a written manual check. A bug fix starts with a failing test that
  reproduces it (see the `bugfix-workflow` and `tdd-workflow` skills).
- Test behaviour through the public interface (an API route, a CLI command, a pure function), not private
  helpers. One reason to fail per test; the name says what should happen.
- Cover the boundaries that hurt: authorization (a role that must be refused), validation, conflicts,
  empty and maximum sizes, time zones (the team's own and UTC), idempotent retries.

## Against what

- Pure logic (rules, calculations, resolvers) gets fast unit tests with no I/O and no mocks.
- **Use a real Postgres for anything the database decides**: driver value types (`bigint` and `NUMERIC` come
  back as strings in Node), `CHECK` and unique constraints, `FOR UPDATE` and concurrency, `COALESCE`,
  migrations. An in-memory store cannot catch these; it returns real numbers and passes while production
  fails.
- Real-Postgres tests skip cleanly when no database is configured, and CI always provides one.
- Mock only what you do not own and cannot run (third-party APIs, the model). Never call a real external
  service from a test.
- An end-to-end test proves the whole chain once; it does not replace the unit and integration tests.

## Data

- Fictional data only (`example.com`, invented people and companies). Never real customer data, CVs or
  invoices, not even anonymised by hand.
- Namespace fixture rows (`zz-test-<file>-…`) and clean them up before and after each test. Tests run in
  parallel: give each test file its own prefix on shared tables, or one file's cleanup deletes another's
  rows mid-test.
- Dates relative to "today", never hard-coded ones that rot.

## CI

- CI runs the same commands as your machine (lint, types, tests, build). A red build is fixed before new
  work starts.
- Do not skip or delete a failing test to get green; fix it, or mark it with the issue that will.
- Flaky tests are bugs: find the shared state or the timing assumption.
