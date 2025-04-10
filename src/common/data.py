"""
data.py
Author: https://github.com/lendrixxx
Description: This file contains mappings and constants related to studio types, locations, and class availability.
"""

from common.class_availability import ClassAvailability
from common.studio_location import StudioLocation
from common.studio_type import StudioType

# Dictionary of studio types and locations
STUDIO_LOCATIONS_MAP = {
    StudioType.Rev: [StudioLocation.Orchard, StudioLocation.TJPG, StudioLocation.Bugis],
    StudioType.Barrys: [StudioLocation.Orchard, StudioLocation.Raffles],
    StudioType.AbsoluteSpin: [
        StudioLocation.Centrepoint,
        StudioLocation.i12,
        StudioLocation.MilleniaWalk,
        StudioLocation.Raffles,
        StudioLocation.StarVista,
    ],
    StudioType.AbsolutePilates: [
        StudioLocation.Centrepoint,
        StudioLocation.GreatWorld,
        StudioLocation.i12,
        StudioLocation.Raffles,
        StudioLocation.StarVista,
    ],
    StudioType.AllySpin: [StudioLocation.CrossStreet],
    StudioType.AllyPilates: [StudioLocation.CrossStreet],
    StudioType.AllyRecovery: [StudioLocation.CrossStreet],
    StudioType.Anarchy: [StudioLocation.Robinson],
}

# Dictionary of availability responses and class availability enum
RESPONSE_AVAILABILITY_MAP = {
    "bookable": ClassAvailability.Available,
    "classfull": ClassAvailability.Waitlist,
    "waitlistfull": ClassAvailability.Full,
    "open": ClassAvailability.Available,
    "waitlist": ClassAvailability.Waitlist,
    "full": ClassAvailability.Waitlist,  # TODO: Confirm session status string
    "closed": ClassAvailability.Available,
    "scheduleCancelled": ClassAvailability.Cancelled,
    "cancelled": ClassAvailability.Cancelled,
}

# Sorted list of days
SORTED_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
