#!/usr/bin/python

import pprint
import sys
from argparse import ArgumentParser

import data_io
import locations
import osrm
import routing


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
    argparser.add_argument(
        "-r",
        "--route",
        dest="fetchroute",
        help="Query OSRM for routing decisions, default: %(default)s",
        action="store_true",
        default=False,
    )
    return argparser


def test_flow(infile="example_data/participants.csv"):
    participants = data_io.read_participants(infile)
    locationlist = locations.get_locations(participants)
    solution = routing.get_route(locationlist, True)
    return participants, locations, solution


def main():
    argparser = init_argument_parser()
    args = argparser.parse_args()

    if args.infile is None or args.outfile is None:
        argparser.print_help()
        sys.exit(0)

    participants = data_io.read_participants(args.infile)
    if args.debug:
        print(f"[DBG] data_io.read_participants({args.infile}):", file=sys.stderr)
        pprint.pprint(participants, stream=sys.stderr)

    locationlist = []
    if args.fetchosm:
        if args.debug:
            print(
                f"Fetching locations for {len(participants)}, this takes about {len(participants)*2} seconds",
                file=sys.stderr,
            )
        locationlist = locations.get_locations(participants, args.debug)
        if args.debug:
            print("[DBG] locations.get_locations(participants):", file=sys.stderr)
            pprint.pprint(locationlist, stream=sys.stderr)

    if args.fetchroute:
        route, length = routing.get_route(locationlist, args.debug)
        if args.outfile:
            if args.outfile == "-":
                print("Route:", route, length, "meters")
                for i in route:
                    print(participants[i])
            elif args.outfile and args.outfile != "-":
                data_io.write_result(participants, route, args.outfile)


if __name__ == "__main__":
    main()
