"""
Provides the container for the application.
"""

from pydantic import BaseModel, ConfigDict

from factorio.clients.release_infos import ReleaseInformationClient
from factorio.configs import FactorioCliSettings
from factorio.services.mod import ModDownloaderService
from factorio.services.server.downloader import ServerDownloaderService
from factorio.services.version_resolver import VersionResolverService


class Container(BaseModel):
    # Settings
    cli_settings: FactorioCliSettings
    # Clients
    release_information_client: ReleaseInformationClient
    # Services
    mod_downloader_service: ModDownloaderService
    server_downloader_service: ServerDownloaderService
    version_resolver_service: VersionResolverService

    model_config = ConfigDict(arbitrary_types_allowed=True)


from .factories import ContainerFactory

_all = [
    "Container",
    "ContainerFactory",
]
