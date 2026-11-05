---
description: Branches, commits and pull requests
---

# Git and pull requests

## Branches

- Never commit to `main`. Every change goes through a branch and a pull request; merging to `main` is
  what releases (semver tag, images), so `main` must always be releasable.
- Branch names: `<issue-or-story-id>-<short-slug>` (for example `PROJ-123-profile-resolver`), or
  `<type>/<slug>` where there is no issue.
- After a squash merge the branch is dead. Rebase stacked work with
  `git rebase --onto origin/main <old-branch-tip>` instead of pushing more commits to it.
- Checkouts can be shared between sessions and agents: check `git status` before every change, stage
  explicit paths (`git add path/to/file`), never `git add -A`.

## Commits

Conventional Commits, imperative and lowercase:

```text
<type>(<scope>): <subject under 72 characters>

Why the change was needed, in a short paragraph.

- What changed, as bullets

Co-Authored-By: <model> <noreply@anthropic.com>
```

- Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`; `!` after the type for a breaking change.
- No vague subjects ("fix bug", "update code"), no past tense, no trailing period, no AI marketing text.
- Always add the `Co-Authored-By` trailer when an AI agent wrote part of the change.
- Never commit secrets, `.env` files or generated build output (generated code that CI checks for drift,
  such as schema types, is the exception).

## Pull requests

- One topic per PR, small enough to review in one sitting.
- Title starts with the issue or story id when there is one.
- Body: what and why, how it was tested, what you could not verify, risks and follow-ups. Link the issue
  (`Closes #n` only when the PR really finishes it, otherwise `Part of #n`). The `pr-description` skill
  writes it.
- An agent always lists the steps it followed in the description, with the outcome of each: planning,
  development, testing, lint and types, security check, maintainability check, documentation and CI. Each
  step is Passed, Failed or Skipped, with the evidence (the command, the test count, the scan) or the reason
  it was skipped. A step is only Passed when it actually ran; a failed or skipped step stays in the list.
- CI must be green (lint, types, tests, build) before review. Do not merge without the approval CODEOWNERS
  requires; never force-push to a branch someone else is reviewing.
- When a change spans repos, ship in dependency order (for example the API first, then its callers,
  then the GitOps repo), so a newer caller degrades instead of breaking. Keep a deprecated alias until every
  caller has moved, and say in the PR when it can be dropped.

## Working with an AI agent

- Agree the plan first for anything larger than a small fix, and work in phases you can review.
- An agent commits, pushes, merges or deploys only when you asked it to. Merging a deploy repo
  (the GitOps repo) is a production change.
- Read the agent's diff like a colleague's: you own what you merge.
