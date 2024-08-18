import logging
from collections import defaultdict
from datetime import datetime
from operator import itemgetter

import line_profiler
import numpy as np
from prettytable import PrettyTable
from scipy.spatial.distance import pdist

from wigle_analyzer.types import Analyzer


class MaxDistancesAnalyzer(Analyzer):
    def __init__(self) -> None:
        self.locations = defaultdict(list)

        self.first_seen = {}
        self.last_seen = {}

    @line_profiler.profile
    def callback_for_each(
        self,
        mac: str,
        lat: str,
        lon: str,
        _altitude: str,
        _accuracy: str,
        time: datetime,
    ):
        point = (float(lat), float(lon))
        self.locations[mac].append(point)

        if mac not in self.first_seen or self.first_seen[mac] > time:
            self.first_seen[mac] = time

        if mac not in self.last_seen or self.last_seen[mac] < time:
            self.last_seen[mac] = time

    @line_profiler.profile
    def write(self, output_file: str | None):
        logging.info('"Writing" table')
        distances = {}

        for mac, points in self.locations.items():
            if len(points) < 2:
                continue

            points = np.array(points)

            max_distance = np.max(pdist(points))

            distances[mac] = max_distance

        sorted_distances = sorted(distances.items(), key=itemgetter(1))

        table = PrettyTable(
            ["MAC", "Num. Points", "Max distance", "First Seen", "Last Seen"]
        )

        rows = [
            [
                mac,
                len(self.locations[mac]),
                distance,
                self.first_seen[mac],
                self.last_seen[mac],
            ]
            for mac, distance in sorted_distances
            if distance > 0.01
        ]
        table.add_rows(rows)

        if output_file is not None:
            if output_file.endswith(".html"):
                string = table.get_html_string()
            elif output_file.endswith(".json"):
                string = table.get_json_string()
            elif output_file.endswith(".csv"):
                string = table.get_csv_string()
            elif output_file.endswith(".tex"):
                string = table.get_latex_string()
            else:
                string = table.get_string()

            with open(output_file, "w+", encoding="utf-8") as f:
                f.write(string)
        else:
            print(table)
