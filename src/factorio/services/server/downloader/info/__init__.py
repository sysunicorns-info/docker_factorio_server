"""
Package for downloading information about Factorio server releases.
"""


from .builders import DownloadInformationBuilder, DownloadInformationBuilderProtocol
from .enums_architecture import Architecture
from .models import DownloadInformation

__all__ = [
    "Architecture",
    "DownloadInformation",
    "DownloadInformationBuilder",
]
