"""

"""

from pydantic import Field
from pydantic_settings import BaseSettings


class FactorioCliSettings(BaseSettings):
    """
    Factorio CLI settings.
    """

    server_download_timeout: int = Field(default=30)

    server_download_checksum: str = Field(
        default="https://www.factorio.com/download/sha256sums/"
    )

    server_download_latest_url: str = Field(
        default="https://www.factorio.com/get-download/latest/headless/linux64"
    )

    server_download_version_url: str = Field(
        default="https://www.factorio.com/get-download/{version}/headless/linux64"
    )

    server_download_version_tag: str = Field(default="{version}")


class FactorioUserAccountSettings(BaseSettings):
    """
    Factorio user account settings.
    """

    username: str
    password: str
