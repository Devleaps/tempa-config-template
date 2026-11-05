---
description: How to build Python services and FastAPI APIs
---

# Python and FastAPI

Applies to every Python repo. User instructions win; otherwise these rules beat generic habits.

## Tooling

- **uv for everything**: `uv add`, `uv sync`, `uv run`. Never pip, poetry or pipenv. In a uv workspace use
  `uv sync --all-packages`; a plain sync can install nothing and let mypy pass on `Any`.
- **ruff** for lint and format, **mypy strict**, **pytest** (no unittest).
- CI runs exactly what you run locally: `uv run pytest -q`, `uv run ruff check .`,
  `uv run ruff format --check .`, `uv run mypy <packages>`. Green tests do not mean typed: run mypy too.
- Python 3.12. Configuration comes from the environment (pydantic-settings), never from code; an invalid
  or missing required setting fails at startup.

## Code

- **Keep it simple.** The simplest thing that works; no abstractions "for later", no design patterns where a
  function will do.
- Type every function and class, including `-> None`. Prefer Pydantic models over raw dicts at boundaries.
- Keep pure logic (rules, calculations, resolvers) free of I/O so it can be tested without mocks.
- Minimal comments: name things well, comment only the non-obvious *why*. Keep existing comments.
- Imports at the top of the module; no imports inside functions.
- Guard clauses and early returns; the happy path last.

## FastAPI

- **Prefer `def` over `async def`.** FastAPI runs sync handlers in its threadpool. Use `async def` only for
  async drivers or real concurrent I/O, and never do blocking work (CPU, sync clients) inside an
  `async def` route: it stalls the event loop and the health probe.
- Pydantic v2 models for request and response bodies; declare `response_model` or return types.
- Dependencies through `Annotated[..., Depends(...)]` aliases (settings, DB session, current user);
  lifespan context managers, not `@app.on_event`.
- Expected errors are `HTTPException` with a specific status (400 validation, 401, 403 role, 404, 409
  conflict, 503 when a dependency is not configured); log details server-side, return a useful message.
- Authorize every route against the caller's identity and roles; fail closed. A service token never
  silently stands in for a user.
- `/healthz` (the process) and `/readyz` (its dependencies) are separate probes.

## Data

- SQLAlchemy 2 with Alembic migrations (see the `postgres` standard). Migrations run as a separate step
  (an init container), not at import time.
- One service layer: REST routes, the UI and an MCP server call the same functions, so a rule lives in one
  place.

## Tests

- pytest with fixtures and factories; tests live in `tests/`, fully typed. Unique test module basenames.
- Test against real Postgres where the behaviour depends on it (types, constraints, concurrency); skip
  cleanly when it is not available. See the `testing` standard.
