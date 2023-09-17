"""
Provides objects for the downloader service
"""

from pydantic import BaseModel, FieldValidationInfo, field_validator

from .enums_architecture import Architecture


class DownloadInformation(BaseModel):
    """
    Class to store download information
    """

    file_name: str
    arch: Architecture
    version: str

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str, info: FieldValidationInfo) -> str:
        """
        Validates the version string
        """
        # Check if the version is in the format 'major.minor.patch'
        _version_split = v.split(".")
        if len(_version_split) != 3:
            raise ValueError("Version must be in the format 'major.minor.patch'")

        # Check if each part of the version is a number
        _major = _version_split[0]
        _minor = _version_split[1]
        _path = _version_split[2]

        if not (_major.isdigit() and _minor.isdigit() and _path.isdigit()):
            raise ValueError(
                "Version must be in the format 'major.minor.patch' as each part must be a number"
            )

        return v
