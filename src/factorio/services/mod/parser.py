"""
Provides a class for building a mod list from a mod-list.json file.
"""

from pathlib import Path

from pydantic import BaseModel, Field


class Mod(BaseModel):
    name: str
    enabled: bool


class ModList(BaseModel):
    mods: list[Mod] = Field(default=[])


class FileNotFound(Exception):
    pass


class FileNotValid(Exception):
    pass


class ModListParser:
    """
    Mod List Builder
    """

    source_file: Path

    def __init__(self, source_file: Path) -> None:
        """
        Initialize the builder
        Raises:
            FileNotFound: If the source file does not exist
        """
        if source_file.exists() is False:
            raise FileNotFound(f"File {source_file} does not exist")

        self.source_file = source_file

    def build(self) -> ModList:
        """
        Build the mod list from the source file
        Raises:
            FileNotValid: If the source file is not valid
        """

        with open(self.source_file, "r", encoding="UTF-8") as f:
            _raw_mod_list = f.read()

        try:
            _mod_list = ModList.model_validate_json(_raw_mod_list)
        except ValueError as error:
            raise FileNotValid(f"File {self.source_file} is not valid") from error

        return _mod_list
