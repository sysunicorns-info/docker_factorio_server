"""
Resolver for mods
"""

from pydantic import BaseModel

from factorio.clients.mod import ModClient
from factorio.configs import FactorioCliSettings

from ..parser import ModList


class ModResolverResult(BaseModel):
    """
    Provides a class for the result of the mod resolver
    """

    pass


class ModResolver:
    """
    Mod Resolver
    Roles:
    - Get Information about the first level of dependencies
    - Introspect the mod list to discover all the dependencies
    """

    original_mod_list: ModList

    _settings: FactorioCliSettings
    _mod_client: ModClient

    def __init__(
        self,
        mod_list: ModList,
        factorio_cli_settings: FactorioCliSettings,
        mod_client: ModClient,
    ) -> None:
        """
        Initialize the resolver
        """
        self._mod_client = mod_client
        self._settings = factorio_cli_settings
        self.original_mod_list = mod_list

    async def _resolve_first_level(self):
        """
        Resolve the first level of dependencies from orginal_mod_list
        """
        pass

    async def resolve(self, target_factorio_version: str) -> ModResolverResult:
        """
        Resolve the mod list
        """
        pass
