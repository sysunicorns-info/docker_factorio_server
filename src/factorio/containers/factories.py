"""
Provides a factory for the container.
"""

from factorio.clients.release_infos import ReleaseInformationClient
from factorio.configs import FactorioCliSettings
from factorio.services.mod import ModDownloaderService
from factorio.services.server.downloader import ServerDownloaderService
from factorio.services.version_resolver import VersionResolverService

from . import Container


class ContainerFactory:
    """
    Build the container with all dependencies.
    """

    def __init__(self) -> None:
        pass

    def build(self) -> Container:
        # Settings
        _cli_settings = FactorioCliSettings()
        # Clients
        _release_information_client = ReleaseInformationClient(_cli_settings)
        # Services
        _mod_downloader_service = ModDownloaderService(_cli_settings)
        _server_downloader_service = ServerDownloaderService(_cli_settings)
        _version_resolver_service = VersionResolverService(
            release_information_client=_release_information_client
        )

        return Container(
            cli_settings=_cli_settings,
            release_information_client=_release_information_client,
            mod_downloader_service=_mod_downloader_service,
            server_downloader_service=_server_downloader_service,
            version_resolver_service=_version_resolver_service,
        )
