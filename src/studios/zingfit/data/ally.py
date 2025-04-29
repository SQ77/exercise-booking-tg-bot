"""
ally.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Ally schedules.
"""

from common.studio_location import StudioLocation
from common.studio_type import StudioType

# URL subdomain
URL_SUBDOMAIN = "ally"

# Max number of weeks that schedule is shown in advance
MAX_SCHEDULE_WEEKS = 3

# Date format of the table heading
TABLE_HEADING_DATE_FORMAT = "%m.%d"

# Dictionary of studio locations and site id params used in get request
LOCATION_TO_SITE_ID_MAP = {
    StudioLocation.CrossStreet: 1,  # Ally shows all locations in single page
}

# Dictionary of room IDs and studio types
ROOM_ID_TO_STUDIO_TYPE_MAP = {
    "1481873008443261972": StudioType.AllySpin,  # Cross Street Ride
    "1750535388780299804": StudioType.AllyPilates,  # Cross Street Reformer Room 1
    "2229597283270263965": StudioType.AllyPilates,  # Cross Street Reformer Room 2
    "2229597531153631005": StudioType.AllyPilates,  # Cross Street Chair Pilates
    "2278264748933907674": StudioType.AllyRecovery,  # Cross Street Recovery Suite
    "2463215192914265745": StudioType.AllySpin,  # Maxwell Ride
    "2463215628249466587": StudioType.AllyPilates,  # Maxwell Reformer
    "2463215890410243679": StudioType.AllyRecovery,  # Maxwell Recovery Suite
    "1993420034390623898": StudioType.AllyEvents,  # Special Events
}

# Dictionary of room IDs and studio locations
ROOM_ID_TO_STUDIO_LOCATION_MAP = {
    "1481873008443261972": StudioLocation.CrossStreet,  # Cross Street Ride
    "1750535388780299804": StudioLocation.CrossStreet,  # Cross Street Reformer Room 1
    "2229597283270263965": StudioLocation.CrossStreet,  # Cross Street Reformer Room 2
    "2229597531153631005": StudioLocation.CrossStreet,  # Cross Street Chair Pilates
    "2278264748933907674": StudioLocation.CrossStreet,  # Cross Street Recovery Suite
    "2463215192914265745": StudioLocation.Maxwell,  # Maxwell Ride
    "2463215628249466587": StudioLocation.Maxwell,  # Maxwell Reformer
    "2463215890410243679": StudioLocation.Maxwell,  # Maxwell Recovery Suite
    "1993420034390623898": StudioLocation.Unknown,  # Special Events
}


# Function to clean class names
def clean_class_name(class_name: str) -> str:
    """
    Removes known location suffixes from a class name.
    """
    return class_name.replace(" (CROSS STREET)", "").replace(" (MAXWELL)", "")
