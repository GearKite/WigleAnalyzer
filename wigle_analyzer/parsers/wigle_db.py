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
    ):
        self.filter_mac = None
        self.last_seen_time = None

        self.con = sqlite3.connect(file_name)
        self.cur = self.con.cursor()

    @line_profiler.profile
    def select_locations(
        self,
        callback: Type[Analyzer.callback_for_each],
        network_bssids: set[str] | None,
    ):
        # Select all locations
        selector = "SELECT bssid, time, lat, lon, altitude, accuracy FROM location"
        parameters = ()

        if network_bssids is not None:
            if len(network_bssids) < 999:
                selector += f" WHERE bssid in ({','.join(['?']*len(network_bssids))})"
                parameters = tuple(network_bssids)

        res = self.cur.execute(selector, parameters)

        locations = res.fetchall()

        # Loop through all the locations and call the callback
        for row in locations:
            mac = row[0]

            if network_bssids is not None and mac not in network_bssids:
                continue

            lat = row[2]
            lon = row[3]
            altitude = row[4]
            accuracy = row[5]

            time = datetime.fromtimestamp(row[1] / 1000)

            callback(mac, lat, lon, altitude, accuracy, time)

    @line_profiler.profile
    def select_networks(
        self,
        filter_mac: str | None,
        last_seen_time: datetime,
    ) -> set[str] | None:
        self.filter_mac = filter_mac
        self.last_seen_time = last_seen_time

        selector = "SELECT bssid FROM network"
        parameters = []

        filters = []

        # Extensible filters (wow)
        if self.last_seen_time is not None:
            filter_selector = "lasttime >= ?"
            filter_parameters = [self.last_seen_time.timestamp() * 1000]

            filters.append(
                (
                    filter_selector,
                    filter_parameters,
                )
            )

        if self.filter_mac is not None:
            filter_selector = "bssid like ?"
            filter_parameters = [self.filter_mac]

            filters.append(
                (
                    filter_selector,
                    filter_parameters,
                )
            )

        if len(filters) > 0:
            selector += " WHERE "
            selector += " AND ".join([s for s, _ in filters])

            for _, p in filters:
                parameters.append(*p)

            res = self.cur.execute(selector, parameters)

            return set([row[0] for row in res.fetchall()])

        return None


def chunk_list(lst, chunk_size):
    """Yield successive chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]
