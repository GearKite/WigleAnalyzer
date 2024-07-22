"""A Wigle database export parser"""

import sqlite3
from datetime import datetime
from typing import Type

import line_profiler

from wigle_analyzer.types import Analyzer, Parser


class DBParser(Parser):
    """A Wigle database export parser"""

    @line_profiler.profile
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
            mac = row[0]
            lat = row[2]
            lon = row[3]
            altitude = row[4]
            accuracy = row[5]

            time = datetime.fromtimestamp(row[1] / 1000)

            callback(mac, lat, lon, altitude, accuracy, time)
