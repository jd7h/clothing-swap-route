import logging
from random import randint

from geopy.distance import distance, geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def build_query_from_participant(participant):
    return ", ".join(
            [participant.get('address'), 
            participant.get('postalcode'), 
            participant.get('city'), 
            participant.get('country')]
        )

def get_locations(participants):
    user_agent = "clothing_loop_{}".format(randint(10000,99999))
    geolocator = Nominatim(user_agent=user_agent)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

    locations = []
    for participant in participants:
        query = build_query_from_participant(participant)
        logging.debug(f"Querying Geo data service for {query}")
        try:
            locations.append(geocode(query))
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
