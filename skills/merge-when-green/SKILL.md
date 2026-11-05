---
name: merge-when-green
description: Wait for a pull request's CI to finish and squash-merge it once every check is green and the required approvals are in. Use when asked to merge a PR when CI is green, or to merge a PR once its checks pass.
---

# Merge when green

Asking for this skill is the request to merge, for the PR you named (or the PR of the current branch). It
covers that one PR only: never merge other PRs on the way, and never treat it as approval for a later one.

**Report to Tempa** when the `tempa` MCP server is there: call `work_step` with `deliver.merged` after the
merge, so the team's work board shows the work as delivered.

## 1. Find the PR

- `gh pr view <number|url|branch> --json number,url,title,state,isDraft,baseRefName,headRefName,mergeable,mergeStateStatus,reviewDecision`
- Stop and say why when it is closed or merged already, a draft, or not mergeable (`CONFLICTING`): conflicts
  are resolved on the branch first, never by merging anyway.

## 2. Check what merging does in this repo

- **Deploy repos (GitOps, infrastructure as code):** merging is a deploy. A prd change only
  merges after the same change is verified on dev; when that is not shown in the PR, ask first.
- **App repos:** merging to `main` releases (semver tag, images). Say so when you report.
- **Public repos** (`gh repo view --json visibility`): ask before merging.

## 3. Wait for CI

- `gh pr checks <number> --watch --interval 15`, with a timeout that fits the repo's CI (default 20
  minutes). Pending is not green: keep waiting until every check has finished.
- **A check fails:** do not merge. Report the failing check with its link and the first relevant lines of
  its log (`gh run view <run-id> --log-failed`). Fix it only when asked.
- **No checks at all:** say so and ask before merging. No CI is not the same as green.
- Never re-run a failed check just to get it green, and never skip one.

## 4. Check approvals

- `reviewDecision` must be `APPROVED`, or empty when the branch protection requires no review.
  `REVIEW_REQUIRED` or `CHANGES_REQUESTED`: stop and say who has to approve (CODEOWNERS).
- Never use `--admin` or anything else that bypasses branch protection.

## 5. Merge

- Update the PR description's **Steps** table first when it has one (`git-and-pr` standard): the CI row
  becomes ✅ Passed with the check names.
- `gh pr merge <number> --squash --delete-branch`. Use the repo's allowed method when squash is disabled
  (`gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed`).
- Confirm with `gh pr view <number> --json state,mergeCommit`: `MERGED` and the merge commit.

## 6. Report

In a few lines: the PR, the checks that passed, the merge commit, and what the merge sets in motion (a
release, a deploy to dev or prd, a promote PR to merge later). If you stopped, say at which step and what
is needed to continue.
