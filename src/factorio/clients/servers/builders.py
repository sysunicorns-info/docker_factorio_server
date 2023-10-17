"""
Checksum builder.
"""

import hashlib
from pathlib import Path
from typing import Callable

from httpx import Response

from .exceptions import ChecksumCalculationException
from .objects import CheckSumsData, CheckSumsFile


class CheckSumDataBuilder:
    """
    Class to build the CheckSumsData object
    from the response of the checksums API.
    """

    _response: Response

    def __init__(self, response: Response) -> None:
        self._response = response

    def build(self) -> CheckSumsData:
        """
        Build the CheckSumsData object.
        """
        _checksums = CheckSumsData()
        _raw_data = self._response.text.split("\n")

        for _raw_line in _raw_data:
            _line = _raw_line.strip()

            if _line == "":
                continue

            _line_split = _line.split("  ")
            _checksum = CheckSumsFile(filename=_line_split[1], checksum=_line_split[0])
            _checksums.checksum_by_filename[_checksum.filename] = _checksum

        return _checksums


class CheckSumFileBuilder:
    """
    Simple class to build a checksum from a file.
    """

    _file_path: Path
    _hash_method: Callable

    def __init__(
        self,
        file_path: Path,
        hash_method: Callable | None,
    ) -> None:
        """
        Initialize the builder.
        """
        self._file_path = file_path
        if hash_method is not None:
            self._hash_method = hashlib.sha256

    def build(self) -> str:
        """
        Build the checksum from the file.
        """
        _hash = self._hash_method()

        try:
            _hash.update(self._file_path.read_bytes())
        except FileNotFoundError as _e:
            raise ChecksumCalculationException() from _e
        except IOError as _e:
            raise ChecksumCalculationException() from _e

        return _hash.hexdigest()
