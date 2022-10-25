#!/usr/bin/python

import csv
import pprint
from os import path

filename = 'example_data/participants.csv'

if not path.isfile(filename):
    print(f"Could not open file {filename}")

with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    participants = [row for row in reader]

pprint.pprint(participants)
