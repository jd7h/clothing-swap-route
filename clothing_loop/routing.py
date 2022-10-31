import numpy as np
from geopy.distance import distance as geopy_distance
from python_tsp.heuristics import solve_tsp_local_search, solve_tsp_simulated_annealing


def distance_matrix(locations):
    """create a distance matrix with the distance from every participant to every participant. We loop over locations twice"""
    return np.array(
        [
            [geopy_distance(location.point, location_.point) for location_ in locations]
            for location in locations
        ]
    )


def tsp_solution(distance_matrix):
    """Try the 2 recommended approaches from the python-tsp manual and return the best result"""
    permutation, distance = solve_tsp_simulated_annealing(distance_matrix)
    permutation2, distance2 = solve_tsp_local_search(
        distance_matrix, x0=permutation, perturbation_scheme="ps3"
    )
    if distance < distance2:
        return permutation, distance
    return permutation2, distance2


def route(locations):
    """Compute (an approximation of) the shortest route through all points, returning at the first point."""
    return tsp_solution(distance_matrix(locations))
