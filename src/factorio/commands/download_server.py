"""
Provide Command to download Factorio Server
"""

from pathlib import Path
from tarfile import TarFile
from typing import Optional

import rich
import typer

from ..configs import FactorioCliSettings
from ..services.server.downloader import (
    FactorioServerDownloaderService as FSDownloaderService,
)


class FactorioServerDownloaderCommand:
    """
    Class representing the Factorio Server Downloader Command.
    """

    VERSION_ERROR_MESSAGE = (
        "Version must be in the format 'major.minor.patch' or 'latest'"
    )

    _factorio_server_downloader_service: FSDownloaderService

    def __init__(
        self,
        factorio_server_downloader_service: FSDownloaderService = FSDownloaderService(
            factorio_cli_settings=FactorioCliSettings()
        ),
    ) -> None:
        """
        Initialize the command and inject the settings
        """
        self._factorio_server_downloader_service = factorio_server_downloader_service

    def _validate_version(self, version: str) -> None:
        """
        Validate the version
        """

        # Latest is always valid
        if version == "latest":
            return

        # Check if version is in the format 'major.minor.patch'
        _version_split = version.split(".")
        if len(_version_split) != 3:
            raise typer.BadParameter(self.VERSION_ERROR_MESSAGE)

        for _version_part in _version_split:
            if not _version_part.isnumeric():
                raise typer.BadParameter(self.VERSION_ERROR_MESSAGE)

        return

    def download_factorio_server(
        self,
        version: str = typer.Argument(default="latest"),
        tmp: Optional[Path] = typer.Option(default=None),
        install_dir: Path = typer.Option(default=Path("/opt/app/factorio")),
    ):
        """
        Download Factorio Server
        """

        # TODO: Add override of the path to download to

        # Validate the version and re-raise in case of error
        # to let Typer handle it
        try:
            self._validate_version(version=version)
        except typer.BadParameter as error:
            raise typer.BadParameter(error)

        if tmp is not None:
            self._factorio_server_downloader_service.set_path(path=tmp)

        # Setup the download directory and download the server
        _is_success, _path_or_error = self._factorio_server_downloader_service.download(
            version=version
        )
        if not _is_success:
            rich.print(
                "[red]Error:[/] Could not download Factorio Server",
            )
            raise typer.Exit(code=1)

        # Install the server
        with TarFile.open(_path_or_error) as _tar_file:
            _tar_file.extractall(path=install_dir)
