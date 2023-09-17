from unittest.mock import Mock, patch

import httpx
import pytest

from factorio.configs import FactorioCliSettings
from factorio.services.server.downloader.checksum import ChecksumProvider, CheckSumsData
from factorio.services.server.errors import ServerError


class TestChecksumProvider:
    def test_download_success(self):
        # Create a mock response object with a status code of 200 and a text attribute
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = "a" * 64 + "  valid_file.tar.xz"

        # Create a mock FactorioCliSettings object with the necessary attributes
        mock_settings = Mock(spec=FactorioCliSettings)
        mock_settings.server_download_checksum = "http://example.com/checksum"
        mock_settings.server_download_timeout = 5.0

        # Patch the httpx.get function to return our mock response object
        with patch("httpx.get", return_value=mock_response):
            provider = ChecksumProvider(factorio_cli_settings=mock_settings)
            success, data = provider.download()

        assert success == True
        assert isinstance(data, CheckSumsData)

    def test_download_failure(self):
        # Create a mock response object with a status code other than 200
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 500

        # Create a mock FactorioCliSettings object with the necessary attributes
        mock_settings = Mock(spec=FactorioCliSettings)
        mock_settings.server_download_checksum = "http://example.com/checksum"
        mock_settings.server_download_timeout = 5.0

        # Patch the httpx.get function to return our mock response object
        with patch("httpx.get", return_value=mock_response):
            provider = ChecksumProvider(factorio_cli_settings=mock_settings)
            success, error = provider.download()

        assert success == False
        assert error == ServerError.UNABLE_TO_GET_CHECKSUM
