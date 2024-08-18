from datetime import datetime
from typing import Type, Union


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
        _time: datetime,
    ):
        pass

    def write(self, _output_file: str):
        pass


class Parser:
    def __init__(
        self,
        file_name: str,
    ):
        pass

    def select_networks(
        self,
        filter_mac: str | None,
        last_seen_time: datetime,
    ) -> set[str] | None:
        pass

    def select_locations(
        self,
        callback: Type[Analyzer.callback_for_each],
        network_bssids: set[str] | None,
    ):
        pass


class Error(Exception):
    pass


class BadInputFormat(Error):
    pass
