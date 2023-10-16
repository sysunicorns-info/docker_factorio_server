"""
Provides the release information client
"""

from pydantic import ValidationError

from factorio.clients.abstracts import AbstractClient

from .exceptions import ReleaseInfoError
from .objects import LatestReleaseInformation


class ReleaseInformationClient(AbstractClient):
    """
    Provides the version information client
    """

    def _setup(self) -> None:
        """
        Setup the client
        """

        self._base_url = self._settings.version_info_base_url
        self._retries = self._settings.version_info_client_reties
        self._timeout = self._settings.version_info_client_timeout

    async def get_latest_information(self) -> LatestReleaseInformation:
        """
        Get the latest release information
        """

        async with self._get_client() as _client:
            _response = await _client.get("/latest-releases")

        if _response.status_code != 200:
            raise RuntimeError("Could not get latest release information")

        try:
            _latest_release_information = LatestReleaseInformation.model_validate_json(
                _response.text
            )
        except (ValidationError, ValueError) as _e:
            raise ReleaseInfoError("API Response Not Valid") from _e

        return _latest_release_information
