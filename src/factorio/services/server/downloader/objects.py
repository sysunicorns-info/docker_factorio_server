"""
Provides objects for the downloader service
"""

from pydantic import BaseModel


class DownloadInformation(BaseModel):
    """
    Class to store download information
    """

    file_name: str
    arch: str
    version: str
