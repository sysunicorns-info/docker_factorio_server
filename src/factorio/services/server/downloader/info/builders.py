"""
Module to build the download information from the response.
"""

from pathlib import Path
from typing import Protocol, TypeVar

import httpx

from .models import DownloadInformation


class DownloadInformationBuilderProtocol(Protocol):
    response: httpx.Response

    def __init__(self, response: httpx.Response) -> None:
        raise NotImplementedError()

    def build(self) -> DownloadInformation:
        raise NotImplementedError()


class DownloadInformationBuilder(DownloadInformationBuilderProtocol):
    """
    Class to build the download information from the response.
    """

    response: httpx.Response

    def __init__(self, response: httpx.Response) -> None:
        """
        initialize the builder.
        """
        self.response = response

    def build(self) -> DownloadInformation:
        """
        Build the information object from the response.
        """
        _file_name = Path(self.response.url.path).name
        _file_name_split = _file_name.replace(".tar.xz", "").split("_")
        return DownloadInformation(
            file_name=_file_name,
            arch=_file_name_split[2],
            version=_file_name_split[3],
        )
