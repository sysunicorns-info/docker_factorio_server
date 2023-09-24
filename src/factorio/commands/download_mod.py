"""

"""

from pathlib import Path
from typing import Optional

import typer

from factorio.configs import FactorioCliSettings
from factorio.services.mod import ModDownloaderService
from factorio.services.mod.builder import FileNotFound, FileNotValid, ModListBuilder


class FactorioModDownloaderCommand:
    """
    Class representing the Factorio Mod Downloader Command.
    """

    def __init__(
        self,
        mod_download_service: ModDownloaderService = ModDownloaderService(
            FactorioCliSettings()
        ),
    ) -> None:
        pass

    def download_factorio_mod(
        self,
        mod_list_path: Path,
        tmp: Optional[Path] = typer.Option(default=None),
        install_dir_path: Path = typer.Option(default=Path("/opt/app/factorio")),
    ) -> None:
        """
        Download the Factorio Mod
        """
        try:
            _mod_list = ModListBuilder(source_file=mod_list_path).build()
        except (FileNotFound, FileNotValid) as e:
            typer.echo(e)
            raise typer.Exit(code=1)
