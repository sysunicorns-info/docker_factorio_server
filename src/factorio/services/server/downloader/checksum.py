"""
Checksum builder.
"""

from httpx import Response

from .objects import CheckSumsData, CheckSumsFile


class CheckSumDataBuilder:
    """
    Class to build the CheckSumsData object.
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
