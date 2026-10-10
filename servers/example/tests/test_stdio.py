"""Test both installed entry points through a real MCP subprocess."""

import os
import sys
from pathlib import Path

import anyio
import pytest
from mcp import Client, StdioServerParameters

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("entrypoint", ["module", "console"])
async def test_stdio_entrypoint(entrypoint: str, tmp_path: Path) -> None:
    command = sys.executable
    args = ["-m", "buvis_mcp_example"]
    if entrypoint == "console":
        command = str(Path(sys.executable).with_name("buvis-mcp-example"))
        args = []
    # The SDK deliberately filters the environment. Forward only coverage's
    # configuration so child processes are measured without inheriting secrets.
    coverage_env = {
        key: os.environ[key]
        for key in ("COVERAGE_PROCESS_CONFIG", "COVERAGE_CORE")
        if key in os.environ
    }
    parameters = StdioServerParameters(command=command, args=args, cwd=tmp_path, env=coverage_env)
    with anyio.fail_after(15):
        async with Client(parameters, read_timeout_seconds=5) as client:
            assert client.server_info is not None
            assert client.server_info.name == "buvis-mcp-example"
            assert [tool.name for tool in (await client.list_tools()).tools] == ["echo"]
            result = await client.call_tool("echo", {"text": "stdio round trip"})
            assert not result.is_error
            assert result.structured_content == {"result": "stdio round trip"}
