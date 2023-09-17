"""
DownloadInformationBuilder unit tests.
"""

import httpx
import pytest

from factorio.services.server.downloader.info import DownloadInfoBuilder


class TestDownloadInformationBuilder:
    """Test the DownloadInformationBuilder class."""

    @pytest.mark.asyncio
    async def test_download_information_builder(self, httpx_mock):
        url = "http://'dl.factorio.com'/releases/factorio_headless_x64_1.1.91.tar.xz"
        httpx_mock.add_response(url=url, method="GET")
        with httpx.Client() as _client:
            response = _client.get(url)

        builder = DownloadInfoBuilder(response)
        download_info = builder.build()

        assert download_info.file_name == "factorio_headless_x64_1.1.91.tar.xz"
        assert download_info.arch == "x64"
        assert download_info.version == "1.1.91"
