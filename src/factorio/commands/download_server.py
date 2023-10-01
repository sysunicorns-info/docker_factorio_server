"""
Provide Command to download Factorio Server
"""

import asyncio
from math import e
from pathlib import Path
from tarfile import TarFile
from typing import Optional

import rich
import typer

from ..clients.release_info.client import ReleaseInformationClient
from ..configs import FactorioCliSettings
from ..services.server.downloader import FactorioServerDownloaderService
from ..services.version_resolver import Version, VersionResolverService


class FactorioServerDownloaderCommand:
    """
    Class representing the Factorio Server Downloader Command.
    """

    VERSION_ERROR_MESSAGE = (
        "Version must be in the format 'major.minor.patch' or 'latest'"
    )

    _factorio_server_downloader_service: FactorioServerDownloaderService
    _version_resolver_service: VersionResolverService

    def __init__(
        self,
        factorio_cli_settings: FactorioCliSettings | None = None,
        factorio_server_downloader_service: FactorioServerDownloaderService
        | None = None,
        version_resolver_service: VersionResolverService | None = None,
    ) -> None:
        """
        Initialize the command and inject the settings
        """

        if factorio_cli_settings is None:
            factorio_cli_settings = FactorioCliSettings()

        if factorio_server_downloader_service is None:
            self._factorio_server_downloader_service = FactorioServerDownloaderService(
                factorio_cli_settings=factorio_cli_settings,
            )

        if version_resolver_service is None:
            self._version_resolver_service = VersionResolverService(
                release_information_client=ReleaseInformationClient(
                    factorio_client_settings=factorio_cli_settings,
                ),
            )

    async def _validate_version(self, version: str) -> Version:
        """
        Validate the version
        Args:
            version (str): The version to validate
        Raises:
            typer.BadParameter: If the version is invalid
        Returns:
            Version: The validated and resolved version
        """

        try:
            _version = await self._version_resolver_service.resolve(version=version)
        except ValueError as error:
            raise typer.BadParameter(error) from error

        return _version

    def download_factorio_server(
        self,
        version: str = typer.Argument(default="latest"),
        tmp: Optional[Path] = typer.Option(default=None),
        install_dir: Path = typer.Option(default=Path("/opt/app/factorio")),
    ):
        """
        Download Factorio Server
        """

        _loop = asyncio.get_event_loop()

        # TODO: Add override of the path to download to

        # Validate the version and re-raise in case of error
        # to let Typer handle it
        try:
            _version = _loop.run_until_complete(self._validate_version(version=version))
        except typer.BadParameter as error:
            raise typer.BadParameter(error)

        rich.print(f"Downloading Factorio Server {_version!r}")

        if tmp is not None:
            self._factorio_server_downloader_service.set_path(path=tmp)

        # Setup the download directory and download the server
        _is_success, _path_or_error = self._factorio_server_downloader_service.download(
            version=_version.version,
        )
        if not _is_success:
            rich.print(
                "[red]Error:[/] Could not download Factorio Server",
            )
            raise typer.Exit(code=1)

        rich.print(f"Factorio Server downloaded to {_path_or_error}")

        # Install the server
        with TarFile.open(_path_or_error) as _tar_file:
            _tar_file.extractall(path=install_dir)

        rich.print(f"Factorio Server installed to {install_dir}")
