---
name: pr-description
description: Write a pull request title and description in a consistent format from the branch's commits and diff. Use when opening or updating a pull request.
---

# Pull request description

When the `tempa` MCP server is there, call `work_step` with `review.pr-open` after the PR is opened, so the
team's work board moves the work to review.

## Gather

1. `git log --oneline origin/main..HEAD` (or the PR's base branch) for the commits.
2. `git diff --stat origin/main...HEAD` and the diff itself for what changed.
3. The issue or story the branch belongs to (branch name `<id>-<slug>`), and its acceptance criteria.
4. What you actually ran in this session for each step in the Steps table below, and its result. Run a
   missing check now rather than guessing its outcome.

## Title

- Start with the issue or story id when there is one: `PROJ-123 · Add the export endpoint`.
- Otherwise a Conventional Commit style summary: `fix: keep archived people out of the time sync`.
- Under 72 characters, imperative, no trailing period.

## Body

Use this template and drop sections that would be empty:

```markdown
Closes #<n>            <!-- or "Part of #<n>" when work remains -->

## Summary
One or two sentences: what this PR does and why.

## Changes
- The meaningful changes, grouped by area, as bullets

## How it was tested
- Tests added or changed; commands run (`uv run pytest`, `pnpm test`, ...)
- Manual checks, with environment

## Steps
| Step | Result | Evidence |
|------|--------|----------|
| Planning | ✅ Passed | Plan agreed / acceptance criteria of #<n> |
| Development | ✅ Passed | What was built |
| Testing | ✅ Passed | `uv run pytest`: 42 passed, 3 new |
| Lint and types | ✅ Passed | `uv run ruff check .`, `uv run mypy app` |
| Security check | ✅ Passed | `gitleaks detect`, no new dependencies, security-basics reviewed |
| Maintainability check | ✅ Passed | Diff reviewed for simplicity, naming, dead code; follows the standards |
| Documentation | ⏭️ Skipped | No user-facing change |
| CI | ❌ Failed | `build` fails on X, fixing in this PR |

## Risks and follow-ups
- Migrations, config or secrets to set, deploy order, breaking changes
- Work left for a follow-up issue

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Rules

- Describe what the reviewer needs, not every file; do not paste the diff.
- The Steps table is required, never dropped: every row is ✅ Passed, ❌ Failed or ⏭️ Skipped. Passed only
  when the step really ran in this work, with the command or check as evidence; Skipped always says why.
  Never leave out or soften a failed step. Update the table when a later push changes a result.
- Be explicit about anything that needs a human: secrets, identity-provider roles, infrastructure, data repair.
- Never include secrets, personal data or customer data in the description.
- Keep the AI attribution line when an agent wrote the PR.
