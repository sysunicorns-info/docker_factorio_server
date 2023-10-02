"""
Package for downloading information about Factorio server releases.
"""


from .builders import DownloadInfoBuilder, IDownloadInfoBuilder
from .enums_architecture import Architecture
from .models import DownloadInformation

__all__ = [
    "Architecture",
    "IDownloadInfoBuilder",
    "DownloadInformation",
    "DownloadInfoBuilder",
]
