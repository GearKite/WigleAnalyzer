import logging
from datetime import datetime
from typing import Type

import line_profiler

from wigle_analyzer.types import Analyzer


class EntryFilter(Analyzer):
    """Validates an entry. If the given entry is valid, calls the callback, otherwise - nothing."""

    def __init__(
        self,
        callback: Type[Analyzer.callback_for_each],
        filter_bad: bool = True,
    ) -> None:
        self.callback = callback

        self.filter_bad = filter_bad

        self.min_date = datetime(year=1971, month=1, day=1)

        logging.debug("Filtering bad entries = %s", filter_bad)

    @line_profiler.profile
    def callback_filter(
        self,
        mac: str,
        lat: str,
        lon: str,
        altitude: str,
        accuracy: str,
        time: datetime,
    ):
        """Callback for each entry"""
        if self.filter_bad:
            if isinstance(lat, str):
                if "∞" in lat:
                    return

            if time < self.min_date:
                return

        self.callback(mac, lat, lon, altitude, accuracy, time)
