"""
Provide Service to download Factorio Server
"""
from pathlib import Path
from typing import Tuple

import httpx
import rich
from pydantic import BaseModel

from factorio.configs import FactorioCliSettings

from .errors import ServerError


class DownloadInformation(BaseModel):
    """
    Class to store download information
    """

    file_name: str
    arch: str
    version: str


class FactorioServerDownloaderService:
    """
    Class to download Factorio Server
    """

    _factorio_cli_settings: FactorioCliSettings
    _target_dir: Path

    DEFAULT_SERVER_DOWNLOAD_NAME = "factorio_headless_x64_{version}.tar.xz"

    def __init__(
        self, factorio_cli_settings: FactorioCliSettings, target_dir: Path
    ) -> None:
        """
        Initialize the service.
        """
        self._factorio_cli_settings = factorio_cli_settings
        self._target_dir = target_dir

    def setup_download_dir(self) -> bool:
        """
        Prepare the download directory.
        """
        self._target_dir.mkdir(parents=True, exist_ok=True)
        return True

    def _extract_information(self, response: httpx.Response) -> DownloadInformation:
        """
        Extract information from the request
        """
        _file_name = Path(response.url.path).name
        _file_name_split = _file_name.replace(".tar.xz", "").split("_")
        _arch = _file_name_split[2]
        _version = _file_name_split[3]
        return DownloadInformation(file_name=_file_name, arch=_arch, version=_version)

    def _build_url(self, version: str) -> str:
        """
        Build the download url for the given version.
        """
        if version == "latest":
            return self._factorio_cli_settings.server_download_latest_url
        else:
            return self._factorio_cli_settings.server_download_version_url.replace(
                self._factorio_cli_settings.server_download_version_tag, version
            )

    def download(self, version: str) -> Tuple[bool, Path | ServerError]:
        """
        Download the server for the given version.
        """
        _url = self._build_url(version)

        rich.print(f"Downloading factorio server with url={_url} for version={version}")

        _response = httpx.get(
            url=_url,
            timeout=self._factorio_cli_settings.server_download_timeout,
            follow_redirects=True,
        )

        if _response.status_code != 200:
            return False, ServerError.UNABLE_TO_DOWNLOAD

        _download_information = self._extract_information(_response)
        rich.print(_download_information)

        return True, self._target_dir / _download_information.file_name
