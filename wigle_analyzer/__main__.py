import argparse
import logging

import coloredlogs
import line_profiler

from wigle_analyzer.analyzers.geojson_map import GeoJsonMap
from wigle_analyzer.analyzers.max_distances import MaxDistancesAnalyzer
from wigle_analyzer.analyzers.point_maps import PointMapsAnalyzer
from wigle_analyzer.filter import EntryFilter
from wigle_analyzer.parsers.wigle_csv import CSVParser
from wigle_analyzer.parsers.wigle_db import DBParser
from wigle_analyzer.types import Analyzer, BadInputFormat, Parser

coloredlogs.install(level=logging.INFO)

ANALYZERS = {
    "geojson_map": GeoJsonMap,
    "max_distances": MaxDistancesAnalyzer,
    "point_maps": PointMapsAnalyzer,
}
PARSERS = {"csv": CSVParser, "sqlite": DBParser}


@line_profiler.profile
def main():
    parser = argparse.ArgumentParser(
        prog="Wigle Analyzer",
        description="Analyzes Wigle database exports",
    )

    parser.add_argument("-i", "--input_file", required=True, nargs="+")
    parser.add_argument("-o", "--output_file")

    parser.add_argument(
        "-f",
        "--input_format",
        choices=PARSERS.keys(),
        help="Parser to use for all input files. Shouldn't be used when using multiple different format input.",
    )
    parser.add_argument("-a", "--analyzer", choices=ANALYZERS.keys(), required=True)

    parser.add_argument("-b", "--keep-bad-entries", action="store_false")

    parser.add_argument("-m", "--mac", help="Centers output on a specific MAC address")

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        coloredlogs.install(level=logging.DEBUG)
    if args.quiet:
        coloredlogs.install(level=logging.ERROR)

    run(args=args)


@line_profiler.profile
def run(args):
    # Create the analyzer
    analyzer = get_analyzer(args)()

    # Final callback
    callback = analyzer.callback_for_each

    # Filter entries
    entry_filter = EntryFilter(callback=callback, filter_bad=args.keep_bad_entries)
    callback = entry_filter.callback_filter

    # Run analysis
    for input_file in args.input_file:
        logging.info("Running parser for %s", input_file)
        reader = get_reader(input_file, args.input_format)
        reader(input_file, callback, filter_mac=args.mac)

    # Write results
    analyzer.write(args.output_file)


def get_analyzer(args) -> Analyzer:
    return ANALYZERS[args.analyzer]


def get_reader(input_file: str, input_format: str | None) -> Parser:
    if input_format is None:
        # Try determining type from file name
        if input_file.endswith(".csv"):
            input_format = "csv"
        elif input_file.endswith(".sqlite"):
            input_format = "sqlite"
        else:
            raise BadInputFormat("Could not determine input format from file name.")

    return PARSERS[input_format]
