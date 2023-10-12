"""
Test the ModListBuilder class
"""
from pathlib import Path

import pytest

from factorio.services.mod.parser import FileNotFound, FileNotValid, ModListParser


def test_parser_mod_list():
    # Create a temporary mod-list.json file for testing
    test_file = Path("test_mod_list.json")
    test_file.write_text(
        '{"mods": ['
        + '{"name": "Mod1", "enabled": "true"}, '
        + '{"name": "Mod2", "enabled": "true"}'
        + "]}"
    )

    # Test building the mod list from the temporary file
    builder = ModListParser(test_file)
    mod_list = builder.build()

    # Check that the mod list was built correctly
    assert len(mod_list.mods) == 2
    assert mod_list.mods[0].name == "Mod1"
    assert mod_list.mods[0].enabled is True
    assert mod_list.mods[1].name == "Mod2"
    assert mod_list.mods[1].enabled is True

    # Clean up the temporary file
    test_file.unlink()


def test_file_not_found():
    # Test that a FileNotFound exception is raised when the source file does not exist
    with pytest.raises(FileNotFound):
        builder = ModListParser(Path("nonexistent_file.json"))
        builder.build()


def test_file_not_valid():
    # Create a temporary mod-list.json file with invalid JSON for testing
    test_file = Path("test_mod_list.json")
    test_file.write_text(
        '{"mods": ['
        + '{"name": "Mod1", "version": "1.0.0"}, '
        + '{"name": "Mod2", "version": "2.0.0"}',
        encoding="utf-8",
    )

    # Test that a FileNotValid exception is raised when the source file is not valid
    with pytest.raises(FileNotValid):
        builder = ModListParser(test_file)
        builder.build()

    # Clean up the temporary file
    test_file.unlink()
