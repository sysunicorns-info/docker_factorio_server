"""
Provides unit tests for the DownloadInformation class.
"""

import pytest

from factorio.services.server.downloader.info import Architecture, DownloadInformation


class TestDownloadInformation:
    """
    Provides unit tests for the DownloadInformation class.
    """

    def test_download_information_creation(self):
        info = DownloadInformation(
            file_name="file_x64_1.0.0.tar.xz", arch=Architecture.X64, version="1.0.0"
        )
        assert info.file_name == "file_x64_1.0.0.tar.xz"
        assert info.arch == Architecture.X64
        assert info.version == "1.0.0"

    def test_version_validator(self):
        # Testing valid version
        version = "1.0.0"
        assert DownloadInformation.validate_version(version, None) == "1.0.0"

        # Testing invalid versions
        with pytest.raises(
            ValueError, match="Version must be in the format 'major.minor.patch'"
        ):
            DownloadInformation.validate_version("1.0", None)

        with pytest.raises(
            ValueError,
            match="Version must be in the format 'major.minor.patch' "
            "as each part must be a number",
        ):
            DownloadInformation.validate_version("1.0.a", None)
