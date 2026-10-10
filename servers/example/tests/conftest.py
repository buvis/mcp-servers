"""Use the SDK's asyncio backend for the example server's protocol tests."""

import pytest


@pytest.fixture
def anyio_backend() -> str:
    """Select the supported backend without requiring Trio."""
    return "asyncio"
