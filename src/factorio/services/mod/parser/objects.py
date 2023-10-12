"""
Pydantic models for mods.
"""

from pydantic import BaseModel, Field


class Mod(BaseModel):
    name: str
    enabled: bool


class ModList(BaseModel):
    mods: list[Mod] = Field(default=[])
