"""
Put your unit tests for factorio.services.server.downloader.checksum.models here.
"""

import re

import pytest

from factorio.services.server.downloader.checksum.models import (
    FILENAME_ACCEPTED_ENDINGS,
    CheckSumsFile,
)


class TestCheckSumsFile:
    """
    Test the CheckSumsFile class
    """

    def test_checksums_file_creation_valid(self):
        for ending in FILENAME_ACCEPTED_ENDINGS:
            filename = f"valid_file{ending}"
            file = CheckSumsFile(filename=filename, checksum="a" * 64)
            assert file.filename == filename
            assert file.checksum == "a" * 64

    def test_filename_validator(self):
        # Test with valid filenames
        for ending in FILENAME_ACCEPTED_ENDINGS:
            filename = f"valid_file{ending}"
            assert CheckSumsFile.validate_filename(filename) == filename

        # Test with an invalid filename
        with pytest.raises(
            ValueError,
            match=re.escape(
                f"Filename must end with one of the following: {FILENAME_ACCEPTED_ENDINGS}"
            ),
        ):
            CheckSumsFile.validate_filename("invalid_file.txt")

    def test_checksum_validator(self):
        # Test with a valid checksum
        assert CheckSumsFile.validate_checksum("a" * 64) == "a" * 64

        # Test with an invalid checksum
        with pytest.raises(ValueError, match="Checksum must be 64 characters long"):
            CheckSumsFile.validate_checksum("a" * 63)
