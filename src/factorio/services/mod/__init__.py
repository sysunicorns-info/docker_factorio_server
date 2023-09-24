"""
Provides the ModDownloaderService class
"""
from factorio.configs import FactorioCliSettings


class ModDownloaderService:
    """
    Provides the Mod Downloader Service
    """

    _factorio_cli_settings: FactorioCliSettings

    def __init__(self, factorio_cli_settings: FactorioCliSettings) -> None:
        """
        Initialize the service and inject the settings
        """
        self._factorio_cli_settings = factorio_cli_settings
