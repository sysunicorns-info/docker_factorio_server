"""
Provides the Mod Downloader Service
"""

from pathlib import Path

from factorio.configs import FactorioCliSettings

from .parser import ModList, ModListParser, ModListParserException


class ModDownloaderService:
    """
    Provides the Mod Downloader Service
    """

    _factorio_cli_settings: FactorioCliSettings
    _mod_list: ModList

    def __init__(self, factorio_cli_settings: FactorioCliSettings) -> None:
        """
        Initialize the service and inject the settings
        """
        self._factorio_cli_settings = factorio_cli_settings

    @classmethod
    def _parse_mod_list(cls, mod_list_path: Path) -> ModList:
        """
        Attempt to parse the mod list
        Args:
            mod_list_path (Path): Path to the mod list
        Raises:
            ModListParserException: If the mod list could not be parsed
        """
        try:
            return ModListParser(source_file=mod_list_path).build()
        except ModListParserException as e:
            raise e

    def download(self, mod_list_path: Path) -> None:
        """
        Download the mods
        """

        # Parse the mod list or raise an exception if it fails
        self._mod_list = self._parse_mod_list(mod_list_path=mod_list_path)
