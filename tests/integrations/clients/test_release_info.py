"""
Validates the ReleaseInformationClient class.
"""

import pytest

from factorio.clients.release_info.client import ReleaseInformationClient
from factorio.clients.release_info.objects import LatestReleaseInformation
from factorio.configs import FactorioCliSettings


@pytest.fixture(name="client")
def fixture_client():
    settings = FactorioCliSettings()
    return ReleaseInformationClient(settings)


@pytest.mark.asyncio
async def test_get_latest_information_success(client: ReleaseInformationClient):
    result = await client.get_latest_information()
    assert isinstance(result, LatestReleaseInformation)


# TODO: Add tests for error cases
