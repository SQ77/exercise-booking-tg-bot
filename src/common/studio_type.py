"""
studio_type.py
Author: https://github.com/lendrixxx
Description: This file defines the StudioType enum which represents the type of a studio.
"""

from enum import Enum


class StudioType(str, Enum):
    """
    Enum representing the type of a studio.
    """

    All = "All"
    AbsoluteSpin = "Absolute (Spin)"
    AbsolutePilates = "Absolute (Pilates)"
    AbsoluteUnknown = "Absolute"
    AllySpin = "Ally (Spin)"
    AllyPilates = "Ally (Pilates)"
    AllyRecovery = "Ally (Recovery)"
    AllyEvents = "Ally (Events)"
    AllyUnknown = "Ally"
    Anarchy = "Anarchy"
    Barrys = "Barrys"
    Rev = "Rev"
    Null = "Null"
