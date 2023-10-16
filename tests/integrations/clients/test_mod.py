"""
Test the mod client with integration tests
"""

import pytest
import rich

from factorio.clients.mods.clients import (
    ModClient,
    ModClientException,
    ModInformation,
    ModInformationFull,
)
from factorio.configs import FactorioCliSettings

MOD_LIST_TEST_PARAMS = [
    pytest.param("far-reach", id="far-reach"),
    pytest.param("factoryplanner", id="factoryplanner"),
    pytest.param("DeadlockBlackRubberBelts", id="DeadlockBlackRubberBelts"),
    pytest.param("AfraidOfTheDark", id="AfraidOfTheDark"),
]


class TestClassIntegrationModClient:
    """
    Test the mod client with integration tests
    """

    MOD_NOT_EXIST_TEST: str = "not-exist-mod"

    @pytest.fixture(name="fixture_factorio_settings")
    def fixture_factorio_settings(self):
        return FactorioCliSettings()

    @pytest.mark.asyncio
    async def test_not_exist_mod(self, fixture_factorio_settings: FactorioCliSettings):
        mod_client = ModClient(factorio_client_settings=fixture_factorio_settings)

        with pytest.raises(ModClientException):
            await mod_client.get_mod_information(self.MOD_NOT_EXIST_TEST)

        with pytest.raises(ModClientException):
            await mod_client.get_mod_information_full(self.MOD_NOT_EXIST_TEST)

    @pytest.mark.parametrize("mod_name", MOD_LIST_TEST_PARAMS)
    @pytest.mark.asyncio
    async def test_get_mod(
        self, fixture_factorio_settings: FactorioCliSettings, mod_name: str
    ):
        mod_client = ModClient(factorio_client_settings=fixture_factorio_settings)

        _mod_information = await mod_client.get_mod_information(mod_name=mod_name)

        assert _mod_information is not None
        assert isinstance(_mod_information, ModInformation)
        assert _mod_information.name == mod_name
        rich.print(_mod_information)

    @pytest.mark.parametrize("mod_name", MOD_LIST_TEST_PARAMS)
    @pytest.mark.asyncio
    async def test_get_mod_full(
        self, fixture_factorio_settings: FactorioCliSettings, mod_name: str
    ):
        mod_client = ModClient(factorio_client_settings=fixture_factorio_settings)
        _mod_information = await mod_client.get_mod_information_full(
            mod_name=mod_name,
        )

        assert _mod_information is not None
        assert isinstance(_mod_information, ModInformationFull)
        assert _mod_information.name == mod_name
        rich.print(_mod_information)
