import csv
import sys
from os import path


def read_participants(filename):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        participants = [row for row in reader]

    return participants


def write_result(participants, route, outfilename):
    new_participants = []
    for i in route:
        new_participants.append(participants[i])
    with open(outfilename, "w", newline="") as csvfile:
        fieldnames = ["address", "postalcode", "city"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_participants:
            writer.writerow(row)
