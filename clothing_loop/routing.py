#!/usr/bin/python

import csv
import sys

from os import path

def read_participants(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        participants = [row for row in reader]

    return participants
