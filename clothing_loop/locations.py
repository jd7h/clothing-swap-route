import logging
from random import randint

from geopy.distance import distance, geodesic
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.location import Location


def build_query_from_participant(participant):
    if not participant.get("country"):
        participant["country"] = "The Netherlands"
    return ", ".join(
        [
            participant.get("address"),
            participant.get("postalcode"),
            participant.get("city"),
            participant.get("country"),
        ]
    )


def get_locations(participants, debug=False):
    user_agent = "clothing_loop_{}".format(randint(10000, 99999))
    geolocator = Nominatim(user_agent=user_agent)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

    locations = []
    for participant in participants:
        query = build_query_from_participant(participant)
        if debug:
            print(f"Querying Geo data service for {query}")
        logging.debug(f"Querying Geo data service for {query}")
        try:
            nominatim_result = geocode(query)
            if is_valid_location(nominatim_result):
                locations.append(nominatim_result)
                if debug:
                    print(f"Nominatim result: {nominatim_result}")
            else:
                raise ValueError(f"No result found for address {query}")
        except GeocoderTimedOut as e:
            logging.info("Geo data service timed out.")
            logging.error(e)
            logging.info(f"Could not get latitude and longitude for {query}")
            continue
        except GeocoderServiceError as e:
            logging.info("Geo data service returned a serious error. Aborting...")
            logging.error(e)
            break
    return locations


def is_valid_location(location):
    return type(location) == Location


def validate_locationlist(participants, locationlist):
    if len(participants) != len(locationlist):
        return False
    for location in locationlist:
        if type(location) != Location:
            return False
    return len(locationlist) == len(set(locationlist))


def location_name(location):
    return str(location)
