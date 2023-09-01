"""
Provide Command to download Factorio Server
"""

from pathlib import Path

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

        # Setup the download directory and download the server
        if not self._factorio_server_downloader_service.download(version=version):
            rich.print(
                "[red]Error:[/] Could not download Factorio Server",
            )
            raise typer.Exit(code=1)
