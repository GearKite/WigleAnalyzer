import logging
import numpy as np
from prettytable import PrettyTable
from scipy.spatial.distance import pdist
from operator import itemgetter

from wigle_analyzer.types import Analyzer


class MaxDistancesAnalyzer(Analyzer):
    def __init__(self) -> None:
        self.locations = {}

    def callback_for_each(
        self,
        mac: str,
        lat: str,
        lon: str,
        _altitude: str,
        _accuracy: str,
        _time: str,
    ):
        if mac not in self.locations:
            self.locations[mac] = []

        point = (float(lat), float(lon))
        self.locations[mac].append(point)

    def write(self, _output_file: str):
        logging.info('"Writing" table')
        distances = {}

        for mac, points in self.locations.items():
            if len(points) < 2:
                continue

            points = np.array(points)

            max_distance = np.max(pdist(points))

            distances[mac] = max_distance

        sorted_distances = sorted(distances.items(), key=itemgetter(1))

        table = PrettyTable(["MAC", "Num. Points", "Max distance"])

        table.add_rows(
            [
                [
                    mac,
                    len(self.locations[mac]),
                    distance,
                ]
                for mac, distance in sorted_distances
            ]
        )

        print(table)
