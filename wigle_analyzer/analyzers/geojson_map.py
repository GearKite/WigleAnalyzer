import logging
from datetime import datetime

import geojson
import line_profiler

from wigle_analyzer.types import Analyzer


class GeoJsonMap(Analyzer):
    def __init__(self) -> None:
        self.features = []

    @line_profiler.profile
    def callback_for_each(
        self,
        mac: str,
        lat: str,
        lon: str,
        altitude: str,
        accuracy: str,
        time: datetime,
    ):
        tags = {
            "mac": mac,
            "altitude": altitude,
            "accuracy": accuracy,
            "time": time.isoformat(),
        }

        point = geojson.Point((float(lon), float(lat)))
        node = geojson.Feature(geometry=point, properties=tags)

        self.features.append(node)

    @line_profiler.profile
    def write(self, output_file: str):
        logging.info("Writing GeoJson feature collection")

        collection = geojson.FeatureCollection(self.features)

        with open(output_file, "w+", encoding="utf-8") as f:
            geojson.dump(collection, f)
