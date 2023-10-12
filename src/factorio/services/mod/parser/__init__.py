"""
Provides a class for building a mod list from a mod-list.json file.
"""

from pathlib import Path

from .exceptions import FileNotFound, FileNotValid
from .objects import ModList


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

        try:
            with open(self.source_file, "r", encoding="UTF-8") as f:
                _raw_mod_list = f.read()
        except ValueError as _e:
            raise FileNotValid(f"File {self.source_file} is not valid") from _e
        except IOError as _e:
            raise FileNotFoundError(f"File {self.source_file} does not exist") from _e

        try:
            _mod_list = ModList.model_validate_json(_raw_mod_list)
        except ValueError as error:
            raise FileNotValid(f"File {self.source_file} is not valid") from error

        return _mod_list
