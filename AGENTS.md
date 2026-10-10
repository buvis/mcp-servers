# buvis MCP servers

Monorepo for buvis servers using the official Python MCP SDK v2, Python 3.12+, and uv.

Read applicable nested `AGENTS.md` files before editing their directory trees if
the host has not loaded them. Root instructions apply throughout the repository.

- `packages/core`: shared process startup; no domain or server dependencies.
- `servers/*`: independent distributions with their own dependencies and entry points.
- Root `pyproject.toml`: workspace, development tools, and shared check configuration.
- `uv.lock`: one resolution for every member.

## Commands

- Setup: `mise run onboard`
- Verify: `mise run check`
- Build: `mise run build`
- Tests only: `mise run run-tests -- [pytest selectors]`
- Format: `mise run format`
- Reference server: `mise run develop`

`tools/` contains forwarding shims; task behavior lives in mise and `tools/lib/`.

## Documentation

- [Architecture](docs/dev/architecture/README.md): boundaries and runtime policy.
- [Adding a server](docs/dev/procedures/add-a-server.md): package and test workflow.
- [Initial research](docs/dev/project-management/intake/new/00001-initial-structure/research.md): SDK and workspace decisions.
- [CI](.github/workflows/ci.yml): verification matrix and isolated wheel checks.
- [Structure migration](docs/dev/project-management/reviews/20261004-structure-repo.md): layout, verification, and deliberate deviations.
