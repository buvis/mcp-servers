"""Check process-wide logging policy without touching pytest's handlers."""

import subprocess
import sys


def test_import_does_not_configure_logging() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import logging; import buvis_mcp_core; " "assert not logging.getLogger().handlers",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    assert result.stdout == ""
    assert result.stderr == ""


def test_stdio_moves_root_logging_to_stderr() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import logging, sys\n"
            "from mcp.server import MCPServer\n"
            "from buvis_mcp_core import run_stdio\n"
            "logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)\n"
            "run_stdio(lambda: MCPServer('logging-test'), log_level=logging.WARNING)\n"
            "logging.info('filtered-message')\n"
            "logging.warning('stderr-message')\n",
        ],
        input="",
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    assert result.stdout == ""
    assert "stderr-message" in result.stderr
    assert "filtered-message" not in result.stderr
