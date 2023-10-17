"""
Server Download Client
"""

from pathlib import Path

from factorio.configs import FactorioCliSettings
from ..abstracts import AbstractClient
from .objects import CheckSumsData
from .builders import CheckSumDataBuilder

class ServerCheckSumClient(AbstractClient):

    _checksum_builder: CheckSumDataBuilder

    def __init__(self, factorio_client_settings: FactorioCliSettings) -> None:
        super().__init__(factorio_client_settings)

    def _setup(self) -> None:
        self._base_url = self._settings.server_checksum_client_base_url
        self._retries = self._settings.server_checksum_client_retries
        self._timeout = self._settings.server_checksum_client_timeout

    def download_checksums(self) -> CheckSumsData:
        pass
        
        


class ServerClient(AbstractClient):

    _server_checksum_client: ServerCheckSumClient

    def __init__(
            self, factorio_client_settings: FactorioCliSettings, 
            server_checksum_client: ServerCheckSumClient| None = None
            ) -> None:
        super().__init__(factorio_client_settings)
        if server_checksum_client is None:
            self._server_checksum_client = ServerCheckSumClient(factorio_client_settings)
        else:
            self._server_checksum_client = server_checksum_client

    def _setup(self) -> None:
        self._base_url = self._settings.server_mod_client_base_url
        self._retries = self._settings.server_mod_client_retries
        self._timeout = self._settings.server_mod_client_timeout

    async def _retrieve_checksums(self) -> None:
        await self._server_checksum_client.retrieve()


    async def download(version: str, target_path: Path) -> bool:


