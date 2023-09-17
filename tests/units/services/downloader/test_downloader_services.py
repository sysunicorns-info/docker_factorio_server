from pathlib import Path
from unittest.mock import Mock, patch

from factorio.configs import FactorioCliSettings
from factorio.services.server.downloader import FactorioServerDownloaderService
from factorio.services.server.downloader.checksum import ChecksumProvider


class TestFactorioServerDownloaderService:
    def test__download_checksums(self):
        # Mock the necessary objects
        settings = FactorioCliSettings(...)
        checksum_provider = ChecksumProvider(factorio_cli_settings=settings)
        downloader_service = FactorioServerDownloaderService(
            factorio_cli_settings=settings
        )

        with patch.object(ChecksumProvider, "download", return_value=(True, None)):
            result, error = downloader_service._download_checksums()

        assert result == True
        assert error == None
