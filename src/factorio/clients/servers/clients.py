"""
"""

from ..abstracts import AbstractClient


class ServerClient(AbstractClient):
    def _setup(self) -> None:
        self._base_url = self._settings.server_mod_client_base_url
        self._retries = self._settings.server_mod_client_retries
        self._timeout = self._settings.server_mod_client_timeout


class ServerCheckSumClient(AbstractClient):
    def _setup(self) -> None:
        self._base_url = self._settings.server_checksum_client_base_url
        self._retries = self._settings.server_checksum_client_retries
        self._timeout = self._settings.server_checksum_client_timeout
