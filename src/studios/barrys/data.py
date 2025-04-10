"""
data.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Barrys schedules.
"""

from common.studio_location import StudioLocation

# Dictionary of location strings from response and studio locations
RESPONSE_LOCATION_TO_STUDIO_LOCATION_MAP = {
    "Orchard": StudioLocation.Orchard,
    "Raffles Place": StudioLocation.Raffles,
}
