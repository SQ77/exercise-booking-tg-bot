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
    AllySpin = "Ally (Spin)"
    AllyPilates = "Ally (Pilates)"
    AllyRecovery = "Ally (Recovery)"
    AllyEvents = "Ally (Events)"
    Anarchy = "Anarchy"
    Barrys = "Barrys"
    Rev = "Rev"
    Unknown = "Unknown"
    Null = "Null"
