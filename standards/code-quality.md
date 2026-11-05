---
description: "Code quality: maintainability, testability and security checks, scaled to the risk of the change"
---

# Code quality

A starting point, not a closed list. Quality means code that stays easy and safe to change; the tools only
serve that. If a better tool fits the stack, a check here does not fit the project, or you see a risk this
file does not mention, use your judgment and say so in the PR.

## What good means

- **ISO/IEC 25010** is the vocabulary: maintainability (testability is part of it), security, reliability.
- **SIG maintainability model** makes it measurable. Its rules of thumb are a nudge, not a gate: units of
  about 15 lines and 4 branch points at most, 4 parameters at most, logic written once, loosely coupled
  modules of balanced size, and no more code than the job needs.
- **OWASP ASVS** is the checklist for authentication, authorization, input handling, sessions, cryptography
  and data protection. When a change touches one of those, name the ASVS chapter you checked in the PR.
- **DORA** (deployment frequency, lead time, change failure rate, time to restore) is the outcome. Quality
  work that makes changes safer or faster is worth doing; work that only moves a metric is not.

## Fit the effort to the risk

| Change | At least |
|--------|----------|
| Copy, docs, config values | linter and formatter |
| Ordinary code | + types, tests for the new behaviour, the project's full CI |
| Auth, roles, outside input, money, personal data, migrations | + SAST on the change, tests for the refusals, an ASVS-minded review in the PR |
| A new dependency, Dockerfile, manifest or Terraform | + a dependency or IaC scan |

- Use what the project already runs first: CI, pre-commit hooks, its linter configuration. Propose a new tool
  only for a clear gap, in its own PR and with the reason; never add one as a side effect of a feature.
- If a Tempa policy denies running a tool, do not work around it (see `security-basics`).

## Maintainability

- Linter and formatter are clean before you call work done: Ruff for Python, ESLint and Prettier for
  TypeScript (`python-fastapi`, `nextjs`). Follow the existing configuration; do not bring your own style.
- Respect architecture rules where they exist (ESLint `no-restricted-imports`, import-linter, pre-commit
  hooks), and propose one when module boundaries are visibly drifting.
- Hotspots, code that is both complex and changed often, deserve the most care.
  `git log --format= --name-only | sort | uniq -c | sort -rn` is a quick first view. Leave a hotspot a
  little better than you found it, within the scope of the task.
- Where SonarQube, SonarCloud or another quality gate is configured, the change passes it.

## Testability

`testing` says what to test and against what. On top of that:

- Code that is hard to test is a design problem, not a testing problem: inject dependencies instead of
  reaching for globals and module singletons, keep pure logic apart from I/O, keep parameter lists short.
- Coverage is a signal, not proof. A test asserts behaviour; a test that only executes lines is noise. Never
  lower a coverage floor or a quality gate to get green.
- Mutation testing (mutmut for Python, Stryker for TypeScript) is the honest check on tests for core domain
  logic: billing, compensation, authorization rules. Suggest it where tests look shallow, and run it on one
  module, not the whole repo.
- Do not weaken an assertion, widen a mock or add a sleep to make a test pass; find out why it fails.

## Security tooling

The rules are in `security-basics`; these tools check them.

- **SAST:** Ruff's `S` rules (flake8-bandit) cover Python without adding a tool; Semgrep covers both
  languages; CodeQL where GitHub code scanning is enabled.
- **Dependencies:** do not add a package with an open advisory. OSV-Scanner reads `uv.lock` and
  `pnpm-lock.yaml`; Dependabot alerts show what is already there. Prefer a few lines of code over a
  dependency for something trivial. Fixing existing alerts is a task of its own: report them, do not bundle
  them into unrelated work.
- **Secrets:** Gitleaks (or TruffleHog) in pre-commit and CI is the safety net; never writing a secret into
  code, config or tests is the defence.
- **Containers and infrastructure as code:** Trivy for images, Dockerfiles, Kubernetes manifests and
  Terraform, Checkov for deeper policy checks, and the container rules in `gitops-deployment`.
- **Running application:** OWASP ZAP against dev, never production, and only with a person's go-ahead. Start
  with the passive baseline scan: an active scan sends attack traffic and writes data into a shared
  environment.
- **Supply chain:** an SBOM per released image (Syft) and OpenSSF Scorecard on the repo help with
  transparency and the EU Cyber Resilience Act. Propose them per repo; do not add them in passing.

## When a check fails

- Fix the cause. A suppression (`# noqa`, `# type: ignore`, `eslint-disable`, a baseline entry) names the
  specific rule and carries a comment saying why.
- Quality problems outside your task: report them in the PR or as an issue instead of fixing them silently.
  Large unrequested refactors make review harder.
- If a recommendation here is wrong for the codebase, say so and why. This standard evolves with the projects,
  through a PR on the Tempa config repo.
