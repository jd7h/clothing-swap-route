import time
from random import randint

import requests

# We explicitly want walking directions, so we use /routed-foot/
OSRM_ENDPOINT = "https://routing.openstreetmap.de/routed-foot/route/v1/driving/"
OSRM_LAST_REQUEST = None

# print statement at import
print(
    "Routing provided by FOSSGIS, data © OpenStreetMap, ODbL, CC-BY-SA, contribute: https://openstreetmap.org/fixthemap"
)


def get_route(locations):
    if len(locations) <= 1:
        raise Exception("Need at least 2 waypoints to get a route")

    formatted_locs = [f"{loc.longitude},{loc.latitude}" for loc in locations]
    uri = ";".join(formatted_locs)
    return osrm_parse(osrm_request(uri))


def get_route_(waypoints):
    if len(waypoints) <= 1:
        raise Exception("Need at least 2 waypoints to get a route")

    for wp in waypoints:
        if not isinstance(wp, dict):
            raise Exception(
                f"Waypoint {wp} is not a dict, expecting {'latitude': 51.48, 'longitude': 0.00}"
            )

    locs = [f"{wp['longitude']},{wp['latitude']}" for wp in waypoints]
    uri = ";".join(locs)
    return osrm_parse(osrm_request(uri))


def osrm_parse(req_json):
    # TODO: parse req_json.code
    # TODO: check for number of returned routes
    # return req_json
    return req_json["routes"][0]["distance"]


def osrm_request(uri):
    global OSRM_LAST_REQUEST

    if OSRM_LAST_REQUEST is None:
        OSRM_LAST_REQUEST = time.time_ns() - int(1e9) - 1

    now = time.time_ns()
    if OSRM_LAST_REQUEST + int(1e9) < now:
        # Requests are limited to 1 per second, wait a bit
        time.sleep(1.2)

    user_agent = "clothing_loop_{}".format(
        randint(10000, 99999)
    )  # TODO: set user-agent globally
    req = requests.get(OSRM_ENDPOINT + uri, headers={"user-agent": user_agent})
    req.raise_for_status()  # raise Exception when status code is 4xx or 5xx
    return req.json()
