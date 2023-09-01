"""
Provide all subCommands for the cli
"""

import typer

from .download_server import FactorioServerDownloaderCommand

# Instanciate the main typer application
typer_application = typer.Typer()

##
# SubCommand SERVER
# Create the subCommand group server
server_group = typer.Typer()

# Setup the subCommands download
server_group.command(name="download")(
    FactorioServerDownloaderCommand().download_factorio_server
)

##

# Add the subCommand server to the main typer application
typer_application.add_typer(server_group, name="server")
