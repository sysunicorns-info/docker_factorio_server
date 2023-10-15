"""
Provides the Factorio Mod Downloader Command.
"""

from pathlib import Path
from typing import Optional

import rich
import typer

from factorio.configs import FactorioCliSettings
from factorio.services.mod import ModDownloaderService


class FactorioModDownloaderCommand:
    """
    Class representing the Factorio Mod Downloader Command.
    """

    _mod_downloader_service: ModDownloaderService

    def __init__(
        self,
        mod_download_service: ModDownloaderService = ModDownloaderService(
            FactorioCliSettings()
        ),
    ) -> None:
        """
        Initialize the command and inject the settings
        """
        self._mod_downloader_service = mod_download_service

    def download_factorio_mod(
        self,
        mod_list_path: Path,
        tmp: Optional[Path] = typer.Option(default=None),
        install_dir: Path = typer.Option(default=Path("/opt/app/factorio")),
    ) -> None:
        """
        Download the Factorio Mod
        """
        del tmp  # unused
        del install_dir  # unused

        self._mod_downloader_service.download(mod_list_path=mod_list_path)
