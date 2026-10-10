"""Exercise the public MCP contract, including SDK validation."""

from importlib.metadata import version

import pytest
from mcp import Client

from buvis_mcp_example.server import create_server

pytestmark = pytest.mark.anyio


async def test_discovery() -> None:
    async with Client(create_server(), raise_exceptions=True) as client:
        assert client.server_info is not None
        assert client.server_info.name == "buvis-mcp-example"
        assert client.server_info.version == version("buvis-mcp-example")
        tools = (await client.list_tools()).tools
        assert [tool.name for tool in tools] == ["echo"]
        assert tools[0].input_schema["required"] == ["text"]
        assert tools[0].annotations is not None
        assert tools[0].annotations.read_only_hint is True
        assert tools[0].annotations.open_world_hint is False


@pytest.mark.parametrize("text", ["hello", "", "Příliš žluťoučký 🐕\nsecond line"])
async def test_echo(text: str) -> None:
    async with Client(create_server(), raise_exceptions=True) as client:
        result = await client.call_tool("echo", {"text": text})
        assert not result.is_error
        assert result.structured_content == {"result": text}


@pytest.mark.parametrize("arguments", [{}, {"text": ["invalid"]}], ids=["missing", "wrong-type"])
async def test_invalid_echo_argument_is_a_tool_error(arguments: dict[str, object]) -> None:
    async with Client(create_server()) as client:
        result = await client.call_tool("echo", arguments)
        assert result.is_error
