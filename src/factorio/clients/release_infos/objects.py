"""
Provides the objects for the release info client
"""

from typing import Any

from pydantic import BaseModel, model_validator


class LatestReleaseInformation(BaseModel):
    """
    Represents the latest release version by channel [experimental, stable]
    """

    experimental: str
    stable: str

    @model_validator(mode="before")
    @classmethod
    def transform_and_validate(cls, data: Any):
        """
        Transforms the data into a dict
        ignoring the other keys (alpha, demo)
        """

        assert isinstance(data, dict)
        assert "experimental" in data
        assert "stable" in data
        assert isinstance(data["experimental"], dict)
        assert isinstance(data["stable"], dict)
        assert "headless" in data["experimental"]
        assert "headless" in data["stable"]

        return {
            "experimental": data["experimental"]["headless"],
            "stable": data["stable"]["headless"],
        }
