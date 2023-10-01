"""
Provides a service for resolving versions of Factorio.
"""

from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel

from factorio.clients.release_info.client import ReleaseInformationClient


class VersionType(StrEnum):
    STATIC = auto()
    DYNAMIC = auto()


class VersionChannel(StrEnum):
    STABLE = auto()
    EXPERIMENTAL = auto()


class VersionTag(StrEnum):
    LATEST = auto()


class Version(BaseModel):
    """
    Represents a version of Factorio.
    """

    version_type: VersionType
    channel: Optional[VersionChannel]
    tag_value: Optional[str]
    version: str

    def __repr__(self) -> str:
        """
        Get the string representation of the version.
        """
        match self.version_type:
            case VersionType.STATIC:
                return f"Version({self.version})"
            case VersionType.DYNAMIC:
                return f"Version({self.channel}-{self.tag_value}={self.version})"


class VersionResolverService:
    """
    Provides a service for resolving versions of Factorio (static and dynamic)
    """

    DYNAMIC_VERSION_ACCEPTABLE = [
        "latest",
        "stable",
        "experimental",
        "stable_latest",
        "experimental_latest",
    ]

    _release_information_client: ReleaseInformationClient

    def __init__(self, release_information_client: ReleaseInformationClient) -> None:
        self._release_information_client = release_information_client

    async def _resolve_dynamic_version(self, version: str) -> Version:
        """
        Resolve a dynamic version to a concrete version.
        Args:
            version: The dynamic version to resolve.
        Returns:
            Version: The concrete version.
        Raises:
            ValueError: If the dynamic version is invalid.
        """

        match (version):
            case "latest":
                _version = "stable_latest"
            case "stable":
                _version = "stable_latest"
            case "experimental":
                _version = "experimental_latest"
            case _:
                _version = version

        try:
            _channel, _tag_value = _version.split("_")
        except ValueError as e:
            raise ValueError(f"Invalid dynamic version: {version}") from e

        _release_information = (
            await self._release_information_client.get_latest_information()
        )

        try:
            _static_version = _release_information[_channel][_tag_value]
        except KeyError as e:
            raise ValueError(f"Invalid dynamic version: {version}") from e

        return Version(
            version_type=VersionType.DYNAMIC,
            channel=_channel,
            tag_value=_tag_value,
            version=_static_version,
        )

    def _resolve_static_version(self, version: str) -> Version:
        """
        Resolve a static version to a concrete version.
        Args:
            version: The static version to resolve.
        Returns:
            Version: The concrete version.
        Raises:
            ValueError: If the static version is invalid.
        """

        _values = version.split(".")

        if len(_values) < 1 or len(_values) > 3:
            raise ValueError(f"Invalid static version: {version}")

        # Sanitize the version values.
        if len(_values) != 3:
            for _ in range(1, 3 - len(_values), 1):
                _values.append("0")

        # Static versions must be numeric.
        for _value in _values:
            if not _value.isdigit():
                raise ValueError(f"Invalid static version: {version}")

        return Version(
            version_type=VersionType.STATIC,
            channel=None,
            tag_value=None,
            version=f"{_values[0]}.{_values[1]}.{_values[2]}",
        )

    async def resolve(self, version: str) -> Version:
        """
        Resolve the version to a concrete version.
        Args:
            version: The version to resolve.
        Returns:
            Version: The concrete version.
        Raises:
            ValueError: If the version is invalid.
        """
        if version in self.DYNAMIC_VERSION_ACCEPTABLE:
            return await self._resolve_dynamic_version(version)
        else:
            return self._resolve_static_version(version)
