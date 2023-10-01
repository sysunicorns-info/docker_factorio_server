"""
Release information client package.
"""

from .client import ReleaseInformationClient
from .exceptions import ReleaseInfoError
from .objects import LatestReleaseInformation

__all__ = [
    "ReleaseInformationClient",
    "ReleaseInfoError",
    "LatestReleaseInformation",
]
