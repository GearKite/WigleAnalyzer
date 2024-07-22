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
        callback: Type[Analyzer.callback_for_each],
        filter_mac: str | None,
    ):
        self.filter = filter_mac is not None

        with open(file_name, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip Wigle info
            next(reader)
            # Skip keys
            next(reader)

            for row in reader:
                mac = row[0]

                if self.filter and mac != filter_mac:
                    logging.debug("Row filtered out by MAC")
                    continue

                lat = row[7]
                lon = row[8]
                altitude = row[9]
                accuracy = row[10]

                time = datetime.fromisoformat(row[3])

                callback(mac, lat, lon, altitude, accuracy, time)
