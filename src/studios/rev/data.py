"""
data.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Rev schedules.
"""

from common.studio_location import StudioLocation

# Dictionary of room name strings from response and studio locations
ROOM_NAME_TO_STUDIO_LOCATION_MAP = {
    "Revolution - Bugis": StudioLocation.Bugis,
    "Revolution - Orchard": StudioLocation.Orchard,
    "Revolution - Tanjong Pagar": StudioLocation.TJPG,
    "TP - Nov 2024": StudioLocation.TJPG,
    "Orchard - Nov 2024": StudioLocation.Orchard,
}

# Dictionary of location strings and site ids
SITE_ID_MAP = {
    "Bugis": "amJoZkVHZTZETDY5NHExRlc0U1A4dz09",
    "Orchard": "SUF6aklTN1BLYWVyNGtGVnBuQ2JiUT09",
    "TJPG": "WHplM0YwQjVCUmZic3RvV3oveFFSQT09",
}
