import numpy as np
from prettytable import PrettyTable
from scipy.spatial.distance import pdist

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
        distances = {}

        for mac, points in self.locations.items():
            if len(points) < 2:
                continue

            points = np.array(points)

            max_distance = np.max(pdist(points))

            distances[mac] = max_distance

        distances = {
            k: v for k, v in sorted(distances.items(), key=lambda item: item[1])
        }

        table = PrettyTable(["MAC", "Num. Points", "Max distance"])

        table.add_rows(
            [
                [
                    mac,
                    len(self.locations[mac]),
                    distance,
                ]
                for mac, distance in distances.items()
            ]
        )

        print(table)
