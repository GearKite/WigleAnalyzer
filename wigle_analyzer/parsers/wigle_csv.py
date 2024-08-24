"""A Wigle csv export parser"""

import csv
import logging
from datetime import datetime
from typing import Type

import line_profiler

from wigle_analyzer.types import Analyzer, Parser


class CSVParser(Parser):
    """A Wigle csv export parser"""

    @line_profiler.profile
    def __init__(
        self,
        file_name: str,
    ):
        self.filter_mac = None
        self.last_seen_time = None
        self.file_name = file_name
        self.filter = False

    @line_profiler.profile
    def select_locations(
        self,
        callback: Type[Analyzer.callback_for_each],
        network_bssids: set[str] | None,
    ):
        with open(self.file_name, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            header_row = next(reader)
            match header_row[0]:
                case "WigleWifi-1.4":
                    ROW_MAC_NUM = 0
                    ROW_LAT_NUM = 6
                    ROW_LON_NUM = 7
                    ROW_ALTITUDE_NUM = 8
                    ROW_ACCURACY_NUM = 9
                case "WigleWifi-1.6":
                    ROW_MAC_NUM = 0
                    ROW_LAT_NUM = 7
                    ROW_LON_NUM = 8
                    ROW_ALTITUDE_NUM = 9
                    ROW_ACCURACY_NUM = 10
                case _:
                    raise (
                        NotImplementedError("This WigleWifi version is not supported!")
                    )

            # Skip keys
            next(reader)

            # Create a generator if given network bssids
            if network_bssids is not None:
                rows = (row for row in reader if row[0] in network_bssids)
            else:
                rows = reader

            for row in rows:
                mac = row[ROW_MAC_NUM]
                lat = row[ROW_LAT_NUM]
                lon = row[ROW_LON_NUM]
                altitude = row[ROW_ALTITUDE_NUM]
                accuracy = row[ROW_ACCURACY_NUM]

                time = datetime.fromisoformat(row[3])

                callback(mac, lat, lon, altitude, accuracy, time)

    @line_profiler.profile
    def select_networks(
        self,
        filter_mac: str | None,
        last_seen_time: datetime,
    ) -> set[str] | None:
        if filter_mac is not None:
            return [filter_mac]

        # TODO: implement
        return None
