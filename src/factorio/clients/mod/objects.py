"""
Provides objects for the Factorio Mod Portal API
"""

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Optional

from pydantic import BaseModel, field_validator, model_validator


class Operator(StrEnum):
    """
    Represents a version comparator
    """

    EQUAL = "="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    NOT_EQUAL = "!="
    OPTIONAL = "?"
    INCOMPATIBLE = "!"


class Dependencies(BaseModel):
    """
    Represents a dependency
    """

    mod_name: str
    comparator: Operator
    version: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def model_validato(cls, data: Any):
        if not isinstance(data, str):
            raise ValueError("mod_name must be a string")

        # Manage the case where the mod is incompatible
        if data.startswith("!"):
            # Mod is incompatible with another mod
            return {
                "mod_name": data[1:],
                "comparator": Operator.INCOMPATIBLE,
                "version": None,
            }

        # Manage the case where the mod is optional
        if data.startswith("?"):
            # Mod is incompatible with another mod
            return {
                "mod_name": data[1:],
                "comparator": Operator.OPTIONAL,
                "version": None,
            }

        # Explode the string into a list
        _split_values = data.split(" ")

        # Manage the case where the mod is base without version
        # meaning that the base version == factorio version
        if len(_split_values) == 1 and _split_values[0] == "base":
            return {
                "mod_name": "base",
                "comparator": Operator.EQUAL,
                "version": None,
            }

        # Nominally, the string must be composed of 3 values mod, comparator, version
        if len(_split_values) != 3:
            raise ValueError(
                "mod_name must be a string with 3 values separated by spaces"
            )

        return {
            "mod_name": _split_values[0],
            "comparator": Operator(_split_values[1]),
            "version": _split_values[2],
        }


class ReleaseInfo(BaseModel):
    """
    Information about a release
    """

    factorio_version: str
    dependencies: Optional[List[Dependencies]] = None

    @field_validator("factorio_version")
    @classmethod
    def validate_factorio_version(cls, value):
        if not isinstance(value, str):
            raise ValueError("factorio_version must be a string")
        if not all(c.isdigit() or c == "." for c in value):
            raise ValueError("factorio_version must be a string of digits and dots")
        return value


class Release(BaseModel):
    """
    Release of Mod
    """

    download_url: str
    file_name: str
    info_json: ReleaseInfo
    released_at: datetime
    sha1: str
    version: str

    @field_validator("released_at", mode="before")
    @classmethod
    def parse_released_at(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    @field_validator("sha1")
    @classmethod
    def validate_sha1(cls, value):
        if not isinstance(value, str):
            raise ValueError("sha1 must be a string")
        if len(value) != 40:
            raise ValueError("sha1 must be 40 characters long")
        if not all(c in "0123456789abcdef" for c in value):
            raise ValueError("sha1 must be a hexadecimal string")
        return value

    @field_validator("download_url")
    @classmethod
    def validate_download_url(cls, value):
        if not isinstance(value, str):
            raise ValueError("download_url must be a string")
        if not value.startswith("/"):
            raise ValueError("download_url must start with /")
        return value

    @field_validator("version")
    @classmethod
    def validate_version(cls, value):
        if not isinstance(value, str):
            raise ValueError("version must be a string")
        if not all(c.isdigit() or c == "." for c in value):
            raise ValueError("version must be a string of digits and dots")
        return value

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, value):
        if not isinstance(value, str):
            raise ValueError("file_name must be a string")
        if not value.endswith(".zip"):
            raise ValueError("file_name must end with .zip")
        return value


class ModInformation(BaseModel):
    """
    Information about a mod
    """

    category: str
    downloads_count: int
    last_highlighted_at: Optional[datetime] = None
    name: str
    owner: str
    releases: List[Release]

    @field_validator("last_highlighted_at", mode="before")
    @classmethod
    def parse_last_highlighted_at(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class License(BaseModel):
    """
    Describes a license
    """

    description: str


class ModInformationFull(BaseModel):
    """
    Full information about a mod
    """

    author: Optional[str] = None
    contact: Optional[str] = None
    description: str
    homepage: Optional[str] = None
    license: Optional[License] = None
    name: str
    releases: List[Release]
    score: float
    summary: str
    thumbnail: Optional[str] = None
    title: str
    updated_at: Optional[datetime] = None

    @field_validator("updated_at", mode="before")
    @classmethod
    def parse_updated_at(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
