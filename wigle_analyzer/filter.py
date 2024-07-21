import logging
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

        logging.debug("Filtering bad entries = %s", filter_bad)

    @line_profiler.profile
    def callback_filter(
        self,
        mac: str,
        lat: str,
        lon: str,
        altitude: str,
        accuracy: str,
        time: str | int,
    ):
        """Callback for each entry"""
        if self.filter_bad:
            if lat == "∞" or lat == "-∞":
                logging.debug("filtering, lat is %s", lat)
                return

            if lon == "∞" or lon == "-∞":
                logging.debug("filtering, lon is %s", lon)
                return

            if isinstance(time, str):
                if time.startswith("1970"):
                    logging.debug("filtering, time is %s", time)
                    return

                if time.startswith("00"):
                    logging.debug("filtering, time is %s", time)
                    return
            else:
                if time < 10000000:
                    logging.debug("filtering, time is %s", time)
                    return

        self.callback(mac, lat, lon, altitude, accuracy, time)
