# Tempa config template

A starting point for your organisation's [Tempa](https://tempa.devleaps.nl) configuration, as code. Tempa
pushes what is in a config like this one (coding standards, skills, policies and MCP endpoints) into every
developer's AI coding agent, resolved per repo through an org tree. This template is the configuration
Devleaps uses, with the organisation-specific parts replaced by examples.

## Quick start

**Upload the ready-made package.** `release/tempa-config.zip` holds the whole config tree. In tempa-web,
open **Config → Drafts → Upload package** and pick the file. The upload becomes a draft you can inspect,
diff against your live config and preview per node before you publish it.

Before you publish, set `id` in `tenant.yaml` to your own tenant id; Tempa refuses a config with another id.
Either change it in the draft (**Files** tab), or build a zip with your id:

```sh
python3 scripts/build_release.py --tenant <your-tenant-id> --out my-config.zip
```

**Or make it your own repo.** Use this repo as a template (or fork it), change the files, and either upload
the zip after each change or point your Tempa tenant at the repo as its config source.

## Make it yours

1. `tenant.yaml`: your tenant `id` and `name`. Keep `groups` commented out until you know your identity
   provider's group ids, and put yourself in the `platform_owner` group first: once a config with groups
   is live, the tenant's bootstrap admins are no longer platform owners.
2. `nodes/`: rename `acme` to your company (or companies), and the teams `platform` and `web` to yours. List
   each team's repos; a repo no node lists, and a user in no group, falls back to `default_node`.
3. `standards/`: read them and adapt them to your stack. They are opinionated (uv, FastAPI, Next.js, pnpm,
   Postgres, GitOps) on purpose; delete what does not apply and switch standards on per node.
4. `policies/`: the guardrails. `universal` is locked at the tenant; add your own bundle for your own rules
   (see `policies/README.md`).
5. Rebuild the release (`python3 scripts/build_release.py`) and commit it with your change; CI checks that
   `release/tempa-config.zip` matches the files.

## Layout

```text
tenant.yaml                          tenant settings, the top of the tree
nodes/<opco>/node.yaml               one folder per node; nesting is the tree
nodes/<opco>/<team>/node.yaml        teams and the repos they own
standards/<name>.md                  coding standards, rendered as rules
skills/<name>/SKILL.md               skills in Agent Skills format
policies/<bundle>/*.rego             Rego guardrails; see policies/README.md
mcp/<name>.yaml                      MCP endpoints (none in the template)
release/tempa-config.zip             the package to upload, built by scripts/build_release.py
.github/workflows/validate.yml       checks the release zip and compiles the policies
```

### The example tree

```text
example (tenant)
└── acme             an operating company
    ├── platform     back-end services, data and deployment (the default team)
    └── web          websites and web apps
```

### What is set where

| Level | Standards | Policies |
|-------|-----------|----------|
| Tenant (`tenant.yaml`) | `git-and-pr`, `security-basics`, `testing`, `api-design`, `code-quality` (extendable) | `universal` **locked**, `default_decision: allow` locked, `allow_external_mcp: true` locked |
| `platform` | + `python-fastapi`, `nextjs`, `postgres`, `gitops-deployment` | + `python_uv` |
| `web` | + `nextjs` | tenant policies (front end, no Python) |

Everyone also gets the skills `tdd-workflow`, `bugfix-workflow`, `pr-description` and `merge-when-green`
(extendable at the tenant), telemetry on (locked), prompt logging off (open), a sync every 15 minutes (open)
and the work board at team level (open).

Mode rules in short: `locked` cannot be changed below, `extendable` can only be added to, `open` can be
added to, removed from or overridden. Guardrails stay tighten-only: below the locked `policies` a team can
add bundles but never remove `universal`.

### The standards

| Standard | About |
|----------|-------|
| `git-and-pr` | branches, Conventional Commits, PRs, cross-repo order, working with an AI agent |
| `security-basics` | secrets, production, identity and authorization, personal data, agents |
| `testing` | what to test, real Postgres over in-memory twins, fictional and namespaced fixtures, CI |
| `api-design` | the API as the single gateway, status codes, idempotency, changing a contract |
| `code-quality` | maintainability, testability and security tooling, scaled to the risk of a change |
| `python-fastapi` | uv, ruff, mypy strict, FastAPI conventions |
| `nextjs` | BFF proxy, typed client, modules, UI and Node services |
| `postgres` | stores, driver types, migrations, append-only tables |
| `gitops-deployment` | releases, GitOps (merging deploys), infrastructure through PR plans |

### The skills

| Skill | What it does |
|-------|--------------|
| `tdd-workflow` | build a feature test first (red, green, refactor) |
| `bugfix-workflow` | reproduce with a failing test, find the root cause, prove the fix |
| `pr-description` | write a PR title and description from the branch's commits and diff |
| `merge-when-green` | wait for CI and squash-merge a PR once it is green and approved |

## Changing things

1. Branch and open a pull request.
2. Edit the YAML or Markdown. Add a standard as `standards/<name>.md`, a skill as `skills/<name>/SKILL.md`
   (frontmatter `name` equal to the folder and a `description`), then switch it on with `add:` in the
   `settings` of the node that should get it.
3. Rebuild the release: `python3 scripts/build_release.py`.
4. Check it against your tenant without changing anything, with the Tempa CLI: `tempa config validate` and
   `tempa config diff`. Then upload the zip (or merge, when Tempa reads this repo).

Add a `CODEOWNERS` file to decide who approves which level: the tenant files and shared assets your
platform owners, `policies/` and `security-basics` your security people, each node its own admins or leads.

## License

MIT, see [LICENSE](LICENSE). The policies come from
[Devleaps/agent-policies-server](https://github.com/Devleaps/agent-policies-server); see
`policies/README.md`.
