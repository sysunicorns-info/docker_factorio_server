from unittest.mock import AsyncMock

import pytest

from factorio.clients.release_info.client import ReleaseInformationClient
from factorio.services.version_resolver import (
    Version,
    VersionChannel,
    VersionResolverService,
    VersionType,
)


@pytest.fixture
def client():
    client = AsyncMock(spec=ReleaseInformationClient)
    client.get_latest_information.return_value = {
        "stable": {"latest": "1.0.0"},
        "experimental": {"latest": "1.1.0"},
    }
    return client


@pytest.fixture
def resolver(client):
    return VersionResolverService(client)


@pytest.mark.asyncio
async def test_resolve_dynamic_version_latest_stable(resolver):
    result = await resolver.resolve("latest")

    assert isinstance(result, Version)
    assert result.version_type == VersionType.DYNAMIC
    assert result.channel == VersionChannel.STABLE
    assert result.tag_value == "latest"
    assert result.version == "1.0.0"


@pytest.mark.asyncio
async def test_resolve_dynamic_version_stable(resolver):
    result = await resolver.resolve("stable")

    assert isinstance(result, Version)
    assert result.version_type == VersionType.DYNAMIC
    assert result.channel == VersionChannel.STABLE
    assert result.tag_value == "latest"
    assert result.version == "1.0.0"


@pytest.mark.asyncio
async def test_resolve_dynamic_version_experimental(resolver):
    result = await resolver.resolve("experimental")

    assert isinstance(result, Version)
    assert result.version_type == VersionType.DYNAMIC
    assert result.channel == VersionChannel.EXPERIMENTAL
    assert result.tag_value == "latest"
    assert result.version == "1.1.0"


@pytest.mark.asyncio
async def test_resolve_static_version(resolver):
    result = await resolver.resolve("1.0.0")

    assert isinstance(result, Version)
    assert result.version_type == VersionType.STATIC
    assert result.channel is None
    assert result.tag_value is None
    assert result.version == "1.0.0"


@pytest.mark.asyncio
async def test_resolve_static_version_invalid(resolver):
    with pytest.raises(ValueError):
        await resolver.resolve("1.0.0.0")


@pytest.mark.asyncio
async def test_resolve_dynamic_version_invalid(resolver):
    with pytest.raises(ValueError):
        await resolver.resolve("invalid")
