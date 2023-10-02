"""
Provide Service to download Factorio Server
"""
import hashlib
from pathlib import Path
from typing import Optional, Tuple

import httpx

from factorio.configs import FactorioCliSettings

from ..errors import ServerError
from .checksum import ChecksumProvider, CheckSumsData
from .info import DownloadInfoBuilder, DownloadInformation, IDownloadInfoBuilder


class FactorioServerDownloaderService:
    """
    Class to download Factorio Server
    """

    _settings: FactorioCliSettings
    _target_dir: Path

    _checksums: CheckSumsData | None = None

    _download_info_builder: IDownloadInfoBuilder

    DEFAULT_SERVER_DOWNLOAD_NAME = "factorio_headless_x64_{version}.tar.xz"

    def __init__(
        self,
        factorio_cli_settings: FactorioCliSettings,
        download_info_builder: IDownloadInfoBuilder = DownloadInfoBuilder,
        target_dir: Optional[Path] = None,
    ) -> None:
        """
        Initialize the service.
        """
        # Set the settings
        self._settings = factorio_cli_settings
        self._download_info_builder = download_info_builder
        self._checksums = None

        # Set the target directory
        if target_dir is None:
            self._target_dir = Path(self._settings.server_download_dir_path_default)
        else:
            self._target_dir = target_dir

    def _download_checksums(self) -> Tuple[bool, None | ServerError]:
        """
        Download the checksums.
        """
        _checksum_provider = ChecksumProvider(factorio_cli_settings=self._settings)
        _success, _checksums_or_error = _checksum_provider.download()
        if not _success:
            return False, _checksums_or_error
        self._checksums = _checksums_or_error
        return True, None

    def _setup_download_dir(self) -> bool:
        """
        Prepare the download directory.
        """
        self._target_dir.mkdir(parents=True, exist_ok=True)
        return True

    def _build_url(self, version: str) -> str:
        """
        Build the download url for the given version.
        """
        if version == "latest":
            return self._settings.server_download_latest_url
        else:
            return self._settings.server_download_version_url.replace(
                self._settings.server_download_version_tag, version
            )

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

    def _retrieve_server(
        self, version: str
    ) -> Tuple[bool, DownloadInformation | ServerError, httpx.Response | None]:
        """
        Retrieve the server for the given version.
        """
        # Build the url
        _url = self._build_url(version)

        # Download the server
        _response = httpx.get(
            url=_url,
            timeout=self._settings.server_download_timeout,
            follow_redirects=True,
        )
        if _response.status_code != 200:
            return False, ServerError.UNABLE_TO_DOWNLOAD, None

        # Extract information
        _download_information: DownloadInformation = self._download_info_builder(
            response=_response
        ).build()

        return True, _download_information, _response

    def download(self, version: str) -> Tuple[bool, Path | ServerError]:
        """
        Download the server for the given version.
        """

        # Setup the download directory
        self._setup_download_dir()

        # Download the checksums
        _is_success, _error = self._download_checksums()
        if _is_success is False:
            return False, _error

        _is_success, _download_information_or_error, _response = self._retrieve_server(
            version
        )

        if not _is_success:
            return False, _download_information_or_error

        # Write the file if not already present
        if not (self._target_dir / _download_information_or_error.file_name).exists():
            with open(
                self._target_dir / _download_information_or_error.file_name, "wb"
            ) as _file:
                _file.write(_response.content)

        # Check if the checksum is correct
        if (
            self._calculate_checksum(
                self._target_dir / _download_information_or_error.file_name
            )
            != self._checksums.checksum_by_filename[
                _download_information_or_error.file_name
            ].checksum
        ):
            return False, ServerError.CHECKSUM_MISMATCH

        return True, self._target_dir / _download_information_or_error.file_name
