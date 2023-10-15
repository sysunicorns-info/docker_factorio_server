"""
Provides exceptions for the ModDownloadService
"""


class ModDownloadServiceException(Exception):
    """
    Base Exception for the ModDownloadService
    """

    pass


class ModDownloadServiceValueError(ModDownloadServiceException):
    """
    Raised when the mod list file is not found
    """

    pass
