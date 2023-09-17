"""
Tests for the CheckSumDataBuilder class.
"""

from unittest.mock import Mock

from httpx import Response

from factorio.services.server.downloader.checksum import CheckSumsData, CheckSumsFile
from factorio.services.server.downloader.checksum.builders import CheckSumDataBuilder


class TestCheckSumDataBuilder:
    """
    Tests for the CheckSumDataBuilder class.
    """

    def test_build(self):
        # Mock response object with text attribute containing checksum data as string
        response = Mock(spec=Response)
        response.text = (
            "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef  "
            "file1.tar.xz\n"
            "fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321  "
            "file2.dmg\n"
        )

        # Instantiate the builder and build the CheckSumsData object
        builder = CheckSumDataBuilder(response)
        checksum_data = builder.build()

        # Assert that checksum_data is an instance of CheckSumsData
        assert isinstance(checksum_data, CheckSumsData)

        # Assert that checksum_data contains the correct CheckSumsFile objects
        assert checksum_data.checksum_by_filename["file1.tar.xz"] == CheckSumsFile(
            filename="file1.tar.xz",
            checksum="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        )
        assert checksum_data.checksum_by_filename["file2.dmg"] == CheckSumsFile(
            filename="file2.dmg",
            checksum="fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
        )
