"""
Provide classes to store checksum data
"""

from typing import Dict

from pydantic import BaseModel


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
