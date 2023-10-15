"""
Provide all subCommands for the cli
"""

from asyncio import Server

import typer

from factorio.configs import FactorioCliSettings

from ..containers import Container, ContainerFactory
from ..services.server.downloader import ServerDownloaderService
from .download_mod import FactorioModDownloaderCommand
from .download_server import FactorioServerDownloaderCommand

# Instanciate the main typer application
typer_application = typer.Typer()

# Initialize Settings and Services
_container = ContainerFactory().build()

# SubCommand MOD - Create the subCommand group mod
mod_group = typer.Typer(name="mod")
# Add the subCommand download to the subCommand group mod
mod_group.command(name="download")(
    FactorioModDownloaderCommand(
        mod_download_service=_container.mod_downloader_service,
    ).download_factorio_mod
)

# SubCommand SERVER - Create the subCommand group server
server_group = typer.Typer(name="server")
# Add the subCommand download to the subCommand group server
server_group.command(name="download")(
    FactorioServerDownloaderCommand(
        factorio_cli_settings=_container.cli_settings,
        factorio_server_downloader_service=_container.server_downloader_service,
        version_resolver_service=_container.version_resolver_service,
    ).download_factorio_server
)

# Add the subCommand groups to the main typer application
typer_application.add_typer(server_group)
typer_application.add_typer(mod_group)
