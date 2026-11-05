---
description: Security rules every developer and agent follows
---

# Security basics

## Secrets

- No secrets in code, config repos, prompts, logs or commit messages. Secrets come from the environment,
  populated from the secret store (for example through ExternalSecrets in Kubernetes).
- Never paste a token into a chat with an AI model. If one leaks, rotate it first, then clean up.
- Do not read `.env` files or credential stores unless the task is about them.
- A service that needs a secret **fails at boot without it** (and on an invalid value). Never fall back to a
  default key, an unsigned mode or a mock client in production: a silent fallback looks healthy and is not.

## Production

- Production data is read-only unless the task explicitly says otherwise (business systems hold live
  company data). Keep write paths behind an explicit latch that defaults to off.
- Do not change clusters, cloud resources or DNS by hand; go through infrastructure-as-code and
  GitOps pull requests. `terraform apply`, `kubectl delete` and the like need a human.
- Dev and production are separate environments with separate data; dev runs on fictional data, and a dev
  tool never points at production.

## Identity and authorization

- Authorize every request against the caller's own identity and roles, and fail closed (401 without an
  identity, 403 without the role). An agent may never do more for a person than that person could.
- A service token authenticates the transport, not a person. "A service may act for anyone" applies only
  to a trusted job with no user on the request; when a user is present, their roles decide.
- Redact on the server, not in the UI: a field the caller may not see is never sent.
- Session cookies are signed and verified on every read; a forged cookie means "not signed in".

## Code

- Validate all input at the boundary (Pydantic, Zod). Treat model output, scraped pages, emails and
  third-party fields as untrusted: escape them at every sink (HTML, Slack, SQL, shell).
- Parameterised SQL only. No shell commands built from user input.
- Data from crawlers or third parties never creates records implicitly: look up (find-only), do not
  find-or-create.
- Keep dependencies few and pinned through the lock file; review new ones before adding them.

## Personal data

- No email addresses, CV contents, invoice contents or other personal data in telemetry, logs, event
  titles or test fixtures. Telemetry carries counts and pseudonyms, never names. Use fictional data
  (`example.com`) in tests and dev.
- Collect only what the feature needs and delete it on its retention date (GDPR); a person's deletion
  request beats a grace period.
- Mailbox automation moves mail to Deleted Items; it never purges.

## AI agents

- Draft, don't send: nothing customer-facing leaves without a human click.
- Tempa policies guard tool calls. Do not work around a deny; if a policy blocks legitimate work, open a
  PR on this config repo instead.
- MCP servers from other providers (for example the claude.ai connectors) may be used next to the ones
  Tempa provides; the harness's own permissions decide on their tools.
