"""
data.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Ally schedules.
"""
from common.studio_type import StudioType

# Dictionary of room IDs and studio types
ROOM_ID_TO_STUDIO_TYPE_MAP = {
  "1481873008443261972": StudioType.AllySpin,     # Ride
  "1750535388780299804": StudioType.AllyPilates,  # Reformer Room 1
  "2229597283270263965": StudioType.AllyPilates,  # Reformer Room 2
  "2229597531153631005": StudioType.AllyPilates,  # Chair Pilates
  "2278264748933907674": StudioType.AllyRecovery, # Recovery Suite
}
