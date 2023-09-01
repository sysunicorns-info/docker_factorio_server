"""
Provides objects for the downloader service
"""

from typing import Dict

from pydantic import BaseModel


class DownloadInformation(BaseModel):
    """
    Class to store download information
    """

    file_name: str
    arch: str
    version: str


class CheckSumsFile(BaseModel):
    """
    Class to store checksum file information
    """

    filename: str
    checksum: str


class CheckSumsData(BaseModel):
    """
    Class to store checksum data
    """

    checksum_by_filename: Dict[str, CheckSumsFile] = {}
