"""
Package for Factorio CLI configs.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class FactorioCliSettings(BaseSettings):
    """
    Factorio CLI settings.
    """

    # Clients/Mods
    server_mod_client_timeout: int = Field(default=10)
    server_mod_client_retries: int = Field(default=3)
    server_mod_client_base_url: str = Field(
        default="https://mods.factorio.com/api/mods"
    )

    # Clients/Servers
    server_download_client_timeout: int = Field(default=10)
    server_download_client_retries: int = Field(default=3)
    server_download_client_base_url: str = Field(
        default="https://www.factorio.com/get-download/"
    )
    server_checksum_client_timeout: int = Field(default=10)
    server_checksum_client_retries: int = Field(default=3)
    server_checksum_client_base_url: str = Field(
        default="https://www.factorio.com/download/sha256sums/"
    )

    # Clients/ReleaseInfos
    version_info_client_timeout: int = Field(default=10)
    version_info_client_reties: int = Field(default=3)
    version_info_base_url: str = Field(default="https://factorio.com/api")

    server_download_dir_path_default: str = Field(default="/tmp/factorio_cli_tmp")


class FactorioUserAccountSettings(BaseSettings):
    """
    Factorio user account settings.
    """

    username: str = Field()
    password: str | None = Field(default=None)
    token: str | None = Field(default=None)
