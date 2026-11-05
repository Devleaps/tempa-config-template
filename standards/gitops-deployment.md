---
description: "How code reaches the clusters: images, GitOps (for example with Argo CD), and infrastructure as code"
---

# Deployment, GitOps and infrastructure

Adapt the repo names and environments below to your own setup; the rules are the point.

## Releases

- A merge to `main` in an app repo computes the next semver, tags it and pushes images to the container
  registry (for example `ghcr.io/<org>/<app>-<service>`). That is all it does: **nothing in an app repo
  deploys.**
- Images of one app move as a set: every service of an app on the same released version.
- Pin image tags; never `latest`, never a floating tag. Third-party images are pinned in their own
  manifests and bumped by hand.

## GitOps (the deploy repo)

- **Merging to `main` in the GitOps repo is a deploy**, usually within minutes (automated sync with self-heal
  and prune). Deleting a manifest deletes the live resource. Never push to `main`; open a PR.
- dev gets image bumps automatically (for example from an image updater, as self-merging PRs); prd follows
  through a promote PR that a human merges after checking dev. Config changes are not promoted: change both
  environments yourself.
- dev and prd are independent copies; diff them when in doubt.
- Every app has a NetworkPolicy (ingress default-deny); secrets come from the secret store (for example
  `ExternalSecret`s), never inline, not even as a placeholder.
- Containers run as non-root, `allowPrivilegeEscalation: false`, capabilities dropped, read-only root
  filesystem with an `emptyDir` where the app needs to write, and resource requests and limits.
- Verify on dev in a browser before promoting to prd: the app loads, the changed path works, the pod logs
  are clean.

## Infrastructure (the infrastructure-as-code repo)

- Terraform (or OpenTofu, Terragrunt) runs **only in CI**: the PR workflow plans every environment and the
  release workflow applies after merge. Never run `terraform` locally against shared state, not even `init`
  or `plan`.
- Prefer changing data (variables, maps in tfvars) over writing new HCL. Change dev and prd together unless
  there is a stated reason not to.
- Read the plan resource by resource. Stop and ask when a plan destroys or replaces an identity-provider
  application, a database, a bucket or a secret, or touches an environment you did not mean to change.
- Secret stores are created empty by infrastructure as code and filled by hand; never write a secret into a
  `.tf` or `.tfvars` file.
