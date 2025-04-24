"""
rev.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Rev schedules.
"""

from common.studio_location import StudioLocation
from common.studio_type import StudioType

# Dictionary of room name strings from response and studio types
ROOM_ID_TO_STUDIO_TYPE_MAP = {
    "Revolution - Bugis": StudioType.Rev,
    "Revolution - Orchard": StudioType.Rev,
    "Revolution - Tanjong Pagar": StudioType.Rev,
    "TP - Nov 2024": StudioType.Rev,
    "Orchard - Nov 2024": StudioType.Rev,
    "TP - Revised April": StudioType.Rev,
    "Revolution - SAFRA Punggol": StudioType.Rev,
}

# Dictionary of room name strings from response and studio locations
ROOM_NAME_TO_STUDIO_LOCATION_MAP = {
    "Revolution - Bugis": StudioLocation.Bugis,
    "Revolution - Orchard": StudioLocation.Orchard,
    "Revolution - Tanjong Pagar": StudioLocation.TJPG,
    "TP - Nov 2024": StudioLocation.TJPG,
    "Orchard - Nov 2024": StudioLocation.Orchard,
    "TP - Revised April": StudioLocation.TJPG,
    "Revolution - SAFRA Punggol": StudioLocation.Unknown,
}

# Dictionary of location strings and site ids
LOCATION_TO_SITE_ID_MAP = {
    "Bugis": "amJoZkVHZTZETDY5NHExRlc0U1A4dz09",
    "Orchard": "SUF6aklTN1BLYWVyNGtGVnBuQ2JiUT09",
    "TJPG": "WHplM0YwQjVCUmZic3RvV3oveFFSQT09",
}
