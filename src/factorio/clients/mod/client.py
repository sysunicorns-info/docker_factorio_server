"""
Provides the client to interact with the mod portal of factorio
"""

from pydantic import ValidationError

from factorio.clients.abstracts import AbstractClient

from .exceptions import ModClientException
from .objects import ModInformation, ModInformationFull


class ModClient(AbstractClient):
    """
    Client to be able to interact with the mod portal of factorio
    """

    def _setup(self) -> None:
        """
        Setup the base url
        """
        self._base_url = self._settings.server_mod_client_base_url
        self._retries = self._settings.server_mod_client_retries

    async def get_mod_information(self, mod_name: str):
        """
        Get the information about a mod

        Args:
            mod_name (str): The name of the mod

        Returns:
            ModInformation: The information about the mod

        Raises:
            ModClientException: If the mod is not found or the information is invalid

        """
        async with self._get_client() as client:
            _response = await client.get(f"/{mod_name}")

        if _response.status_code != 200:
            raise ModClientException("Mod not found")

        try:
            _mod_information = ModInformation.model_validate_json(_response.text)
        except ValidationError as e:
            raise ModClientException("Mod information is invalid") from e

        return _mod_information

    async def get_mod_information_full(self, mod_name: str) -> ModInformationFull:
        """
        Get the full information about a mod

        Args:
            mod_name (str): The name of the mod

        Returns:
            ModInformationFull: The full information about the mod

        Raises:
            ModClientException: If the mod is not found or the information is invalid

        """

        async with self._get_client() as client:
            _response = await client.get(f"/{mod_name}/full")

        if _response.status_code != 200:
            raise ModClientException("Mod not found")

        try:
            _mod_information = ModInformationFull.model_validate_json(_response.text)
        except ValidationError as e:
            raise ModClientException("Mod information is invalid") from e

        return _mod_information
