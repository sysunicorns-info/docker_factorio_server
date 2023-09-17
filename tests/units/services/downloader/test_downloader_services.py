"""
Tests for the FactorioServerDownloaderService class.
"""
from unittest.mock import patch

from factorio.configs import FactorioCliSettings
from factorio.services.server.downloader import FactorioServerDownloaderService
from factorio.services.server.downloader.checksum import ChecksumProvider


class TestFactorioServerDownloaderService:
    """
    Tests for the FactorioServerDownloaderService class.
    """

    def test__download_checksums(self):
        # Mock the necessary objects
        settings = FactorioCliSettings(...)
        downloader_service = FactorioServerDownloaderService(
            factorio_cli_settings=settings
        )

        with patch.object(ChecksumProvider, "download", return_value=(True, None)):
            # pylint: disable=protected-access
            result, error = downloader_service._download_checksums()

        assert result is True
        assert error is None
