---
name: tdd-workflow
description: Build a feature or behaviour change test first (red, green, refactor). Use when adding functionality, changing behaviour or implementing a story's acceptance criteria.
---

# Test-driven workflow

Work in small red-green-refactor loops. Each acceptance criterion gets at least one test, or a written
manual check when a test is impossible.

**Report to Tempa** when the `tempa` MCP server is there, so the team's work board shows where the work is:
call `work_item` with the issue or story URL (or key) when you start, then `work_step` at each stage below:
`refine.understand` (1), `develop.test` (2), `develop.build` (3 and 4), `review.pr-open` once the PR is open.

## 1. Understand

- Read the issue or story completely, and the code around the change. Find the existing tests for that
  area and copy their style (fixtures, factories, naming).
- Write down the behaviours to build as a short list of test names before writing code.

## 2. Red

- Write one failing test for the next behaviour. Test behaviour through the public interface, not
  implementation details.
- Run it and **see it fail for the right reason** (an assertion, not an import error or a typo).

## 3. Green

- Write the simplest code that makes the test pass. No extra features, no abstractions for later.
- Run the test, then the whole suite for that package.

## 4. Refactor

- Remove duplication and improve names while everything is green. Keep pure logic free of I/O.
- Run the full checks the repo's CI runs:
  - Python: `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy ...`
  - TypeScript: `pnpm lint && pnpm typecheck && pnpm test`

## 5. Repeat and finish

- Loop until every behaviour on the list has a passing test.
- Add a regression test for each edge case you found on the way (empty input, missing permission,
  duplicates, time zones, string-typed numbers from the database).
- Commit in small steps with Conventional Commit messages; open the PR with the `pr-description` skill.

## Rules

- Never weaken or delete a test to make it pass; if the test is wrong, say why in the commit.
- Do not mock what you own; use real Postgres for database behaviour where the repo has pg tests.
- Green tests do not mean typed: always run the type checker too.
