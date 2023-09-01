"""
Provide Service to download Factorio Server
"""
import hashlib
from pathlib import Path
from typing import Optional, Tuple

import httpx
import rich

from factorio.configs import FactorioCliSettings

from ..errors import ServerError
from .checksum import CheckSumDataBuilder, CheckSumsData
from .objects import DownloadInformation


class FactorioServerDownloaderService:
    """
    Class to download Factorio Server
    """

    _factorio_cli_settings: FactorioCliSettings
    _target_dir: Path

    _checksums: CheckSumsData | None = None

    DEFAULT_SERVER_DOWNLOAD_NAME = "factorio_headless_x64_{version}.tar.xz"

    def __init__(
        self,
        factorio_cli_settings: FactorioCliSettings,
        target_dir: Optional[Path] = None,
    ) -> None:
        """
        Initialize the service.
        """
        # Set the settings
        self._factorio_cli_settings = factorio_cli_settings

        self._checksums = None

        # Set the target directory
        if target_dir is None:
            self._target_dir = Path(
                self._factorio_cli_settings.server_download_dir_path_default
            )
        else:
            self._target_dir = target_dir

    def _setup_download_dir(self) -> bool:
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

    def _download_checksums(self) -> None:
        """
        Acquire the checksums.
        """

        _response = httpx.get(
            url=self._factorio_cli_settings.server_download_checksum,
            timeout=self._factorio_cli_settings.server_download_timeout,
        )

        if _response.status_code != 200:
            return False, ServerError.UNABLE_TO_GET_CHECKSUM

        self._checksums = CheckSumDataBuilder(response=_response).build()

    def set_path(self, path: Path) -> None:
        """
        Set the target path.
        """
        self._target_dir = path

    def _calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate the checksum for the given file.
        """
        _hash = hashlib.sha256()
        _hash.update(file_path.read_bytes())
        return _hash.hexdigest()

    def _check_if_file_exist_in_target_dir_with_correct_checksum(
        self, file_name: str
    ) -> bool:
        """
        Check if the file already exists in the target directory.
        """
        if not (self._target_dir / file_name).exists():
            return False

        if self._checksums.checksum_by_filename[
            file_name
        ].checksum != self._calculate_checksum(self._target_dir / file_name):
            return False

        return True

    def download(self, version: str) -> Tuple[bool, Path | ServerError]:
        """
        Download the server for the given version.
        """

        # Setup the download directory
        self._setup_download_dir()

        # Download the checksums
        self._download_checksums()

        # Build the url
        _url = self._build_url(version)
        rich.print(f"Downloading factorio server with url={_url} for version={version}")

        # Download the server
        _response = httpx.get(
            url=_url,
            timeout=self._factorio_cli_settings.server_download_timeout,
            follow_redirects=True,
        )
        if _response.status_code != 200:
            return False, ServerError.UNABLE_TO_DOWNLOAD

        # Extract information
        _download_information = self._extract_information(_response)
        rich.print(_download_information)

        # Check if the file already exists
        if self._check_if_file_exist_in_target_dir_with_correct_checksum(
            _download_information.file_name
        ):
            rich.print(
                f"File {_download_information.file_name} already exists in {_download_information.file_name}"
            )
            return True, self._target_dir / _download_information.file_name

        # Write the file
        with open(self._target_dir / _download_information.file_name, "wb") as _file:
            _file.write(_response.content)

        # Check if the checksum is correct
        if (
            self._calculate_checksum(self._target_dir / _download_information.file_name)
            != self._checksums.checksum_by_filename[
                _download_information.file_name
            ].checksum
        ):
            return False, ServerError.CHECKSUM_MISMATCH

        return True, self._target_dir / _download_information.file_name
