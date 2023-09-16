"""
Package for checksum data an doperation
"""

from typing import Tuple

import httpx

from factorio.configs import FactorioCliSettings

from ...errors import ServerError
from .builder import CheckSumDataBuilder
from .objects import CheckSumsData, CheckSumsFile


class ChecksumProvider:
    """
    Download the checksums.
    """

    _factorio_cli_settings: FactorioCliSettings

    def __init__(self, factorio_cli_settings: FactorioCliSettings) -> None:
        self._factorio_cli_settings = factorio_cli_settings

    def download(self) -> Tuple[bool, CheckSumsData | ServerError]:
        """
        Perform the download of the checksums.
        """

        _response = httpx.get(
            url=self._factorio_cli_settings.server_download_checksum,
            timeout=self._factorio_cli_settings.server_download_timeout,
        )

        if _response.status_code != 200:
            return False, ServerError.UNABLE_TO_GET_CHECKSUM

        return True, CheckSumDataBuilder(response=_response).build()


__all__ = [
    "CheckSumDataBuilder",
    "ChecksumProvider",
    "CheckSumsData",
    "CheckSumsFile",
]
