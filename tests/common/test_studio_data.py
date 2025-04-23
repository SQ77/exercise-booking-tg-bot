"""
test_studio_data.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the StudioData studio.
"""

from common.studio_data import StudioData
from common.studio_location import StudioLocation


def test_studiodata_equality() -> None:
    """
    Test that two identical StudioData objects are considered equal.
    """
    locations = [StudioLocation.Raffles, StudioLocation.Orchard]
    instructors = ["Barrys Instructor", "Anarchy Instructor", "Rev Instructor"]

    studio1 = StudioData(locations=locations, instructors=instructors)
    studio2 = StudioData(locations=locations, instructors=instructors)

    assert studio1 == studio2, "Studios should be equal"


def test_studiodata_inequality() -> None:
    """
    Test that different StudioData objects are not equal.
    """
    studio1_locations = [StudioLocation.Raffles, StudioLocation.Orchard]
    studio1_instructors = ["Barrys Instructor", "Anarchy Instructor", "Rev Instructor"]
    studio2_locations = [StudioLocation.GreatWorld, StudioLocation.i12]
    studio2_instructors = ["Barrys Instructor", "Anarchy Instructor", "Rev Instructor"]

    studio1 = StudioData(locations=studio1_locations, instructors=studio1_instructors)
    studio2 = StudioData(locations=studio2_locations, instructors=studio2_instructors)

    assert studio1 != studio2, "Studios should not be equal"


def test_studiodata_inequality_non_studio_data_object() -> None:
    """
    Test inequality with a StudioData object and a non-StudioData object.
    """
    locations = [StudioLocation.Raffles, StudioLocation.Orchard]
    instructors = ["Barrys Instructor", "Anarchy Instructor", "Rev Instructor"]

    studio_data = StudioData(locations=locations, instructors=instructors)
    non_studio_data = 1

    assert studio_data != non_studio_data, "Studios should not be equal"
