"""
test_class_data.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the ClassData class.
"""

from common.capacity_info import CapacityInfo
from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


def test_classdata_name_escaping():
    """
    Test that ClassData escapes special characters in name.
    """
    class_data = ClassData(
        studio=StudioType.Rev,
        location=StudioLocation.Orchard,
        name="Test *Class_ `Spin`",
        instructor="Rev Instructor",
        time="08:00 AM",
        availability=ClassAvailability.Available,
        capacity_info=CapacityInfo(),
    )

    assert class_data.name == r"Test \*Class\_ \`Spin\`"


def test_classdata_equality():
    """
    Test that two identical ClassData objects are considered equal.

    Class availability and capacity are ignored for equality check.

    """
    studio = StudioType.Barrys
    location = StudioLocation.Raffles
    class_name = "Arms & Abs"
    instructor = "Barrys Instructor"
    class_time = ("04:15 PM",)
    availability = ClassAvailability.Available
    capacity_info = CapacityInfo()

    class1 = ClassData(studio, location, class_name, instructor, class_time, availability, capacity_info)
    class2 = ClassData(studio, location, class_name, instructor, class_time, availability, capacity_info)

    assert class1 == class2, "Classes should be equal"

    class2.availability = ClassAvailability.Waitlist

    assert class1 == class2, "Class availability should not be checked for equality"

    class2.availability = class1.availability
    class2.capacity_info = CapacityInfo(
        has_info=True,
        capacity=20,
        remaining=5,
        waitlist_capacity=10,
        waitlist_reserved=0,
    )

    assert class1 == class2, "Class capacity info should not be checked for equality"


def test_classdata_inequality():
    """
    Test that different ClassData objects are not equal.
    """
    studio = StudioType.AllySpin
    location = StudioLocation.CrossStreet
    availability = ClassAvailability.Available
    capacity_info = CapacityInfo()

    class1 = ClassData(studio, location, "RIDE: ESSENTIALS 50", "Instructor A", "08:00 AM", availability, capacity_info)
    class2 = ClassData(studio, location, "RIDE: SIGNATURE 60", "Instructor B", "09:00 AM", availability, capacity_info)

    assert class1 != class2, "Classes should not be equal"


def test_classdata_comparison():
    """
    Test that ClassData objects are correctly ordered by time.
    """
    studio = StudioType.AbsolutePilates
    location = StudioLocation.Centrepoint
    availability = ClassAvailability.Available
    capacity_info = CapacityInfo()

    class1 = ClassData(
        studio, location, "PILATES (Wunda Chair) Essential 60", "Instructor A", "08:00 AM", availability, capacity_info
    )
    class2 = ClassData(
        studio,
        location,
        "PILATES (Reformer) Fit & Tone 60 - Rm1",
        "Instructor B",
        "09:00 AM",
        availability,
        capacity_info,
    )

    assert class1 < class2, "Classes should only be compared by class time"

    class1.time = "01:00 PM"

    assert class2 < class1, "Expected class 2 (09:00 AM) to be less than class 1 (01:00 PM)"
