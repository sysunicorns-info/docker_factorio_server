"""
Provides custom exceptions for the mod parser.
"""


class ModListParserException(Exception):
    """
    Base Exception for the ModListParser
    """

    pass


class ModListParserFileNotFound(ModListParserException):
    """
    Raised when the mod list file is not found
    """

    pass


class ModListParserFileNotValid(ModListParserException):
    """
    Raised when the mod list file is not valid
    """

    pass
