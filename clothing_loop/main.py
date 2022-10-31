#!/usr/bin/python

import pprint
import sys
from argparse import ArgumentParser

from data_io import read_participants
from locations import get_locations


def init_argument_parser():
    argparser = ArgumentParser()
    # -h/--help is automatically provided by ArgumentParser
    argparser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Output intermediate debugging lines to standard error, default: %(default)s",
        default=False,
    )
    argparser.add_argument(
        "-g",
        "--get-osm-data",
        dest="fetchosm",
        action="store_true",
        help="Query OpenStreetMaps for address details, default: %(default)s",
        default=False,
    )
    argparser.add_argument(
        "-i",
        "--input",
        dest="infile",
        help="Read the CSV input from this filename, or - for standard input, default: %(default)s",
    )
    argparser.add_argument(
        "-o",
        "--output",
        dest="outfile",
        help="Store the output CSV in this filename, or - for standard output, default: %(default)s",
        default="-",
    )
    return argparser


def main():
    argparser = init_argument_parser()
    args = argparser.parse_args()

    if args.infile is None or args.outfile is None:
        argparser.print_help()
        sys.exit(0)

    participants = read_participants(args.infile)
    if args.debug:
        print(f"[DBG] read_participants({args.infile}):", file=sys.stderr)
        pprint.pprint(participants, stream=sys.stderr)

    if args.fetchosm:
        if args.debug:
            print(
                f"Fetching locations for {len(participants)}, this takes about {len(participants)*2} seconds",
                file=sys.stderr,
            )
        locations = get_locations(participants)
        if args.debug:
            print("[DBG] get_locations(participants):", file=sys.stderr)
            pprint.pprint(locations, stream=sys.stderr)


if __name__ == "__main__":
    main()
