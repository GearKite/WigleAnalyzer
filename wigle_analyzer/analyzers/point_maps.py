import logging

import geojson

from wigle_analyzer.types import Analyzer


class PointMapsAnalyzer(Analyzer):
    def __init__(self) -> None:
        self.features = {}

    def callback_for_each(
        self,
        mac: str,
        lat: str,
        lon: str,
        altitude: str,
        accuracy: str,
        time: str,
    ):
        tags = {"mac": mac, "altitude": altitude, "accuracy": accuracy, "time": time}

        point = geojson.Point((float(lon), float(lat)))
        node = geojson.Feature(geometry=point, properties=tags)

        if mac not in self.features:
            self.features[mac] = []

        self.features[mac].append(node)

    def write(self, output_dir: str):
        logging.info("Writing GeoJson feature collection")

        for mac, features in self.features.items():
            output_file = f"{output_dir}/{mac}.geojson"
            logging.info("Writing %s", output_file)

            collection = geojson.FeatureCollection(features)

            with open(output_file, "w+", encoding="utf-8") as f:
                geojson.dump(collection, f)
