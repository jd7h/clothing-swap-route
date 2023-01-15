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
    for idx, i in enumerate(route):
        next_stop = participants[i]
        next_stop["order"] = idx + 1
        new_participants.append(next_stop)
    with open(outfilename, "w", newline="") as csvfile:
        fieldnames = [k for k in participants[0].keys() if k != "order"] + ["order"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_participants:
            writer.writerow(row)
