---
description: How to design HTTP APIs and their contracts
---

# API design

## One gateway

- The API is the single source of business rules: validation, status semantics, events and
  authorization. The UI, agents and MCP servers all go through it; nobody else touches the database.
- Everything the UI can do is available through the API (and an MCP tool), with the same role checks.
- Keep the contract in one place: JSON Schema or OpenAPI, with generated types for every client.

## Requests and responses

- Validate every body and query at the edge; reject with 400 and a message that says what is wrong.
- Status codes mean something: 401 no identity, 403 missing role or outside your scope, 404 not found, 409
  conflict (duplicate, wrong state, a record something else still points at), 422 understood but cannot be
  done, 503 a dependency is not configured or down.
- Status fields hold real states only; a transition with side effects gets its own endpoint (promote,
  publish, revoke) instead of a generic status write.
- Partial updates are tri-state: absent leaves the field, `null` clears it, a value sets it.
- Lists are filtered and paged on the server (`limit`, a cursor such as `before`), and counted on the server,
  never by counting a capped page on the client.
- Large binaries are never part of list or detail responses; expose `has_x` and a dedicated download
  endpoint.

## Safe to call again

- Writes that agents or webhooks repeat are idempotent: dedupe on a natural key (for example
  `(kind, subject)` with a partial unique index) and return the existing record.
- A redelivered webhook or a retried job must not create a second record or a second side effect.
- Derive what can be derived (age, priority, health, ownership) on read instead of storing it.

## Changing a contract

- Additive changes only on a live API. To rename, add the new name, keep the old one as a deprecated alias
  that answers the same, and remove it when every caller (often an agent in another repo, on its own
  release schedule) has moved.
- Ship the provider before the caller, so a newer caller meets an older API gracefully.
- Document every endpoint's role, inputs and errors next to the code; the MCP instructions mention new
  workflows.
