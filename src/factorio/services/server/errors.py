"""
Provides errors for the server service.
"""

from enum import StrEnum, auto


class ServerError(StrEnum):
    """
    Server errors.
    """

    GENERIC = auto()
    UNABLE_TO_DOWNLOAD = auto()
    UNABLE_TO_GET_CHECKSUM = auto()
    CHECKSUM_MISMATCH = auto()
