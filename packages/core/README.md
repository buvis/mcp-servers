# buvis-mcp-core

Shared runtime for buvis servers using the official Python MCP SDK v2.

`run_stdio(create_server)` configures process-wide logging on stderr, calls the
supplied factory, and runs its SDK `MCPServer` over stdio. Logging is configured
before construction because the SDK can log during initialization.
Call it only from an executable entry point: it replaces
existing root logging handlers so logs cannot corrupt the stdout protocol stream.
Use `log_level=logging.DEBUG` to change the default INFO level.

Construct servers and register tools directly with the SDK. Core has no import-time
logging configuration, domain tools, credentials, or server dependencies.
