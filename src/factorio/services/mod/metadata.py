"""
Provides services for Factorio mod metadata.
"""

from pydantic import BaseModel

from factorio.configs import FactorioCliSettings


class ModMetadata(BaseModel):
    """
    Represents the metadata for a Factorio mod.
    """

    name: str


class FactorioModMetadaService:
    """
    Represents a Factorio Mod Metadata Service.
    """

    _factorio_settings: FactorioCliSettings

    def __init__(self, factorio_settings: FactorioCliSettings) -> None:
        self._factorio_settings = factorio_settings

    def get_mod_metadata(self, mod_name: str) -> ModMetadata:
        """
        Get the metadata for a Factorio mod.
        """
        pass
