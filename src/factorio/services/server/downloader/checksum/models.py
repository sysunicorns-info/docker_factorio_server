"""
Provide classes to store checksum data
"""

from typing import Dict

from pydantic import BaseModel, field_validator

FILENAME_ACCEPTED_ENDINGS = [".tar.xz", ".dmg", ".zip", ".exe"]


class CheckSumsFile(BaseModel):
    """
    Class to store checksum file information
    """

    filename: str
    checksum: str

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        """
        Validate the filename
        """

        if not any(value.endswith(ending) for ending in FILENAME_ACCEPTED_ENDINGS):
            raise ValueError(
                f"Filename must end with one of the following: "
                f"{FILENAME_ACCEPTED_ENDINGS}"
            )
        return value

    @field_validator("checksum")
    @classmethod
    def validate_checksum(cls, value: str) -> str:
        """
        Validate the checksum
        """
        if len(value) != 64:
            raise ValueError("Checksum must be 64 characters long")
        return value


class CheckSumsData(BaseModel):
    """
    Class to store checksum data
    """

    checksum_by_filename: Dict[str, CheckSumsFile] = {}
