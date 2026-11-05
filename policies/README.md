# Policies

Rego bundles in the agent-policies style. The folder name is the bundle name and must match the Rego
`package` (`package universal`, `package python_uv`, `package helpers...`).

| Bundle      | Assigned where                                                     | What it does                                                        |
| ----------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| `universal` | `tenant.yaml`, **locked**: every developer, no level can remove it | Safe defaults for shell, git, gh, cloud CLIs, file operations, etc. |
| `python_uv` | the Python teams (`platform` in the example tree)                  | Steers Python work to uv (no pip, poetry or bare python)            |
| `helpers`   | not assigned; a library the other bundles import                   | `data.helpers` utility functions                                    |

## Origin

`universal`, `python_uv` and `helpers` come from the open source
[Devleaps/agent-policies-server](https://github.com/Devleaps/agent-policies-server), directory `policies/`,
at commit [`db0f739e7875e3f8821aac0c87ea443a62af2917`](https://github.com/Devleaps/agent-policies-server/tree/db0f739e7875e3f8821aac0c87ea443a62af2917/policies),
with two changes so they also compile with OPA (Rego v1): an unused `every` key in
`universal/file_operations.rego` and a missing `import data.helpers` in `universal/vale.rego`. Organisation
specific domains were taken out of the `curl` allowlist in `universal/network.rego`; add your own there.

Your own rules go in a new bundle (for example `policies/myorg/`, `package myorg`), so the upstream copies
stay easy to refresh.

## Check

```sh
opa check policies
```

Tempa validates the bundles again when you upload or publish the config.
