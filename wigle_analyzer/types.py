from typing import Type


class Analyzer:
    def __init__(self) -> None:
        pass

    def callback_for_each(
        self,
        _mac: str,
        _lat: str,
        _lon: str,
        _altitude: str,
        _accuracy: str,
        _time: str,
    ):
        pass

    def write(self, _output_file: str):
        pass


class Parser:
    def __init__(
        self,
        file_name: str,
        callback: Type[Analyzer.callback_for_each],
        filter_mac: str | None,
    ):
        pass


class Error(Exception):
    pass


class BadInputFormat(Error):
    pass
