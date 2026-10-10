We need to establish this as a monorepo for development of buvis MCP servers. Use official Python SDK v2 for building MCP servers. Share a common core package to reuse in all MCP servers.

Implementation delivered 2026-10-03: uv workspace, official SDK v2.3.0 lock,
shared core, reference server, tests, CI, and documentation. See
[research and verification](research.md).

Local setup is complete: Git is initialized on `master`, mise is trusted, and the
structure checker passes (verified 2026-10-04).
Historical intake: implementation was delivered without a formal spec. It remains
in `new/` because `processed/` means a spec exists, not that work is complete.
Do not re-execute this idea as new work; see the verification evidence in the
[structure migration report](../../../reviews/20261004-structure-repo.md).
