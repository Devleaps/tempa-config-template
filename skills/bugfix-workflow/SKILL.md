---
name: bugfix-workflow
description: Fix a bug by reproducing it with a failing test, finding the root cause and proving the fix. Use when something is broken, a test fails, or a user reports wrong behaviour.
---

# Bugfix workflow

Fix causes, not symptoms. A bug is done when a test that failed before the fix passes after it.

**Report to Tempa** when the `tempa` MCP server is there, so the team's work board shows where the fix is:
call `work_item` with the bug's issue URL (or key) when you start, then `work_step` at each stage below:
`refine.understand` (1 and 2), `develop.test` once the failing test is written, `develop.build` (3),
`review.pr-open` once the PR is open (4).

## 1. Reproduce

- Restate the bug: expected behaviour, actual behaviour, where it was seen (environment, version, input).
- Reproduce it locally or in dev, never by experimenting on production data.
- Write a **failing test** that shows the bug. If it cannot be automated, write down exact manual steps.

## 2. Find the root cause

- Read the code path end to end; check logs, recent commits (`git log -p`, `git blame`) and related
  issues.
- Form one hypothesis at a time and check it with evidence (a log line, a debugger, a smaller test).
- Look for the same mistake elsewhere: a missed conversion or wrong default usually exists in more than
  one place.
- Check the silent-failure suspects first: wrong environment variable or mode, a fallback that returns
  plausible data, a string where a number was expected, a time zone.

## 3. Fix

- Make the smallest change that removes the cause. Do not refactor unrelated code in the same PR.
- Run the new test (now green) and the full suite, linter and type checker.
- Add tests for neighbouring cases the root cause could also break.

## 4. Explain

- Commit as `fix: <what is fixed>`, with a body saying what caused it and why the fix is right.
- In the PR: symptom, root cause, fix, how it was verified, and any data that needs repair.
- If the bug reached production, note whether a follow-up is needed (data cleanup, monitoring, a policy
  or standard change) and open an issue for it rather than growing this PR.

## Rules

- Never silence an error, skip a test or catch-and-ignore an exception to make a bug "go away".
- Fail closed: a fix in auth or permissions must never widen access as a side effect.
