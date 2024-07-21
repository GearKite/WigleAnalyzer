"""A Wigle database export parser"""

import csv
import logging
import sqlite3
from typing import Type

from wigle_analyzer.types import Analyzer, Parser


class DBParser(Parser):
    """A Wigle database export parser"""

    def __init__(
        self,
        file_name: str,
        callback: Type[Analyzer.callback_for_each],
        filter_mac: str | None,
    ):
        con = sqlite3.connect(file_name)
        cur = con.cursor()

        selector = "SELECT bssid, time, lat, lon, altitude, accuracy FROM location"
        parameters = ()

        if filter_mac is not None:
            selector += " WHERE bssid like ?"
            parameters = (filter_mac,)

        res = cur.execute(selector, parameters)

        locations = res.fetchall()

        for row in locations:
            logging.debug("Reading row: %s", row)

            mac = row[0]
            time = row[1]
            lat = row[2]
            lon = row[3]
            altitude = row[4]
            accuracy = row[5]

            callback(mac, lat, lon, altitude, accuracy, time)
