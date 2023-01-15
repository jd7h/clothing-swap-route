import pprint
from itertools import combinations

import locations
import numpy as np
import osrm
from geopy.distance import distance as geopy_distance
from python_tsp.heuristics import solve_tsp_local_search, solve_tsp_simulated_annealing


def straight_line_distance_matrix(locationlist):
    """create a distance matrix with the distance from every participant to every participant. We use
    geopy to compute the distance between points as a straight line. We loop over locations twice."""
    return np.array(
        [
            [
                geopy_distance(location.point, location_.point)
                for location_ in locationlist
            ]
            for location in locationlist
        ]
    )


def query_osrm_distance_matrix(locationlist, debug=False):
    # create a distance matrix
    comb = combinations(
        locationlist, 2
    )  # create all combinations of waypoints of length 2
    comb_list = list(comb)  # should be n*n - n/2

    if debug:
        print(f"{len(comb_list)} items in distance matrix")
        print(
            f"Querying these from OSRM will take about {(2 * len(comb_list)) / 60} minutes."
        )
    distances = {}

    for c in comb_list:
        distance = osrm.get_route(c)
        location_name_A = locations.location_name(c[0])
        location_name_B = locations.location_name(c[1])
        if debug:
            print(location_name_A, "====>", location_name_B, ":", distance, "meters")
        if location_name_A not in distances:
            distances[location_name_A] = {}
        distances[location_name_A][location_name_B] = distance
        if location_name_B not in distances:
            distances[location_name_B] = {}
        distances[location_name_B][location_name_A] = distance

    for location in locationlist:
        name = locations.location_name(location)
        distances[name][name] = 0
    return distances


def osrm_to_distance_matrix(locationlist, osrm_result, debug=False):
    """create a distance matrix with the distance from every participant to every participant using the results of OSRM queries."""
    return np.array(
        [
            [
                osrm_result[locations.location_name(location_A)][
                    locations.location_name(location_B)
                ]
                for location_B in locationlist
            ]
            for location_A in locationlist
        ]
    )


def tsp_solution(distance_matrix, debug=False):
    """Try the 2 recommended approaches from the python-tsp manual and return the best result"""
    if debug:
        print("Computing traveling salesman problem using distance matrix:")
        pprint.pprint(distance_matrix)
    permutation, distance = solve_tsp_simulated_annealing(distance_matrix)
    permutation2, distance2 = solve_tsp_local_search(
        distance_matrix, x0=permutation, perturbation_scheme="ps3"
    )
    if debug:
        print(f"Permutation 1: {permutation}, {distance}")
        print(f"Permutation 2: {permutation2}, {distance2}")
    if distance < distance2:
        return permutation, distance
    return permutation2, distance2


def get_route(locationlist, debug=False):
    """Compute (an approximation of) the shortest route through all points, returning at the first point."""
    osrm_result = query_osrm_distance_matrix(locationlist, debug)
    distance_matrix = osrm_to_distance_matrix(locationlist, osrm_result, debug)
    return tsp_solution(distance_matrix, debug)
