"""
data.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Ally schedules.
"""

from common.studio_location import StudioLocation
from common.studio_type import StudioType

# Dictionary of room IDs and studio types
ROOM_ID_TO_STUDIO_TYPE_MAP = {
    "1481873008443261972": StudioType.AllySpin,  # Cross Street Ride
    "1750535388780299804": StudioType.AllyPilates,  # Cross Street Reformer Room 1
    "2229597283270263965": StudioType.AllyPilates,  # Cross Street Reformer Room 2
    "2229597531153631005": StudioType.AllyPilates,  # Cross Street Chair Pilates
    "2278264748933907674": StudioType.AllyRecovery,  # Cross Street Recovery Suite
    "1993420034390623898": StudioType.AllyEvents,  # Special Events
}

# Dictionary of room IDs and studio locations
ROOM_ID_TO_STUDIO_LOCATION_MAP = {
    "1481873008443261972": StudioLocation.CrossStreet,  # Cross Street Ride
    "1750535388780299804": StudioLocation.CrossStreet,  # Cross Street Reformer Room 1
    "2229597283270263965": StudioLocation.CrossStreet,  # Cross Street Reformer Room 2
    "2229597531153631005": StudioLocation.CrossStreet,  # Cross Street Chair Pilates
    "2278264748933907674": StudioLocation.CrossStreet,  # Cross Street Recovery Suite
    "1993420034390623898": StudioLocation.Unknown,  # Special Events
}
