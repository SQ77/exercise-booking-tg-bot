"""
test_query_data.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the QueryData class.
"""

from datetime import datetime

from common.query_data import QueryData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


def test_query_data_initialization(sample_query_data: QueryData) -> None:
    """
    Test QueryData initializes correctly with given values.

    Args:
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_query_data.current_studio == StudioType.AbsoluteSpin
    assert sample_query_data.weeks == 3
    assert sample_query_data.days == ["Monday", "Wednesday", "Friday"]
    assert len(sample_query_data.start_times) == 1
    assert sample_query_data.start_times[0] == (
        datetime.strptime("06:00", "%H:%M"),
        datetime.strptime("07:00", "%H:%M"),
    )
    assert sample_query_data.class_name_filter == "RIDE"


def test_get_studio_locations(sample_query_data: QueryData) -> None:
    """
    Test getting studio locations for a given studio.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_query_data.get_studio_locations(StudioType.AbsoluteSpin) == [
        StudioLocation.Orchard,
        StudioLocation.Raffles,
    ]
    assert sample_query_data.get_studio_locations(StudioType.Rev) == [StudioLocation.Bugis]
    assert sample_query_data.get_studio_locations(StudioType.Anarchy) == []


def test_get_selected_studios_str(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted string of selected studios.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_query_data.get_selected_studios_str() == "Absolute (Spin) - Orchard, Raffles\nRev - Bugis"
    assert sample_empty_query_data.get_selected_days_str() == "None"


def test_get_selected_days_str(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted string of selected days.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_selected_days_str() == "None"
    assert sample_query_data.get_selected_days_str() == "Monday, Wednesday, Friday"

    all_days_query = QueryData(
        studios={},
        current_studio=StudioType.AbsoluteSpin,
        weeks=2,
        days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        start_times=[],
        class_name_filter="",
    )
    assert all_days_query.get_selected_days_str() == "All"


def test_get_selected_time_str(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted string of selected time ranges.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_selected_time_str() == "All"
    assert sample_query_data.get_selected_time_str() == "0600 - 0700"


def test_get_selected_class_name_filter_str(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted class name filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_selected_class_name_filter_str() == "None"
    assert sample_query_data.get_selected_class_name_filter_str() == "RIDE"


def test_get_selected_instructors_str(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted string of selected instructors.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_selected_instructors_str() == "None"
    assert sample_query_data.get_selected_instructors_str() == (
        "Absolute (Spin): Absolute Instructor, Spin Instructor\nRev: Rev Instructor"
    )


def test_get_query_str_include_studio(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with studios filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_query_str(include_studio=True) == "Studio(s):\nNone\n"
    assert sample_query_data.get_query_str(include_studio=True) == (
        "Studio(s):\nAbsolute (Spin) - Orchard, Raffles\nRev - Bugis\n"
    )


def test_get_query_str_include_instructors(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with instructors filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_query_str(include_instructors=True) == "Instructor(s):\nNone\n"
    assert sample_query_data.get_query_str(include_instructors=True) == (
        "Instructor(s):\nAbsolute (Spin): Absolute Instructor, Spin Instructor\nRev: Rev Instructor\n"
    )


def test_get_query_str_include_weeks(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with weeks filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_query_str(include_weeks=True) == "Week(s): 2\n"
    assert sample_query_data.get_query_str(include_weeks=True) == "Week(s): 3\n"


def test_get_query_str_include_days(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with days filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_query_str(include_days=True) == "Day(s): None\n"
    assert sample_query_data.get_query_str(include_days=True) == "Day(s): Monday, Wednesday, Friday\n"


def test_get_query_str_include_time(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with time filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_query_str(include_time=True) == "Timeslot(s):\nAll\n"
    assert sample_query_data.get_query_str(include_time=True) == "Timeslot(s):\n0600 - 0700\n"


def test_get_query_str_include_class_name(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with class name filter.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    assert sample_empty_query_data.get_query_str(include_class_name_filter=True) == "Class Name Filter: None\n"
    assert sample_query_data.get_query_str(include_class_name_filter=True) == "Class Name Filter: RIDE\n"


def test_get_query_str_include_all(sample_empty_query_data: QueryData, sample_query_data: QueryData) -> None:
    """
    Test getting formatted query string with all filters.

    Args:
      - sample_empty_query_data (QueryData): Empty dictionary of studios to use.
      - sample_query_data (QueryData): Dictionary of selected studios and locations and instructors to use.

    """
    empty_query_expected_output = (
        "Studio(s):\nNone\n\n"
        "Instructor(s):\nNone\n\n"
        "Week(s): 2\n\n"
        "Day(s): None\n\n"
        "Timeslot(s):\nAll\n\n"
        "Class Name Filter: None\n"
    )
    assert (
        sample_empty_query_data.get_query_str(
            include_studio=True,
            include_instructors=True,
            include_weeks=True,
            include_days=True,
            include_time=True,
            include_class_name_filter=True,
        )
        == empty_query_expected_output
    )

    query_expected_output = (
        "Studio(s):\nAbsolute (Spin) - Orchard, Raffles\nRev - Bugis\n\n"
        "Instructor(s):\nAbsolute (Spin): Absolute Instructor, Spin Instructor\nRev: Rev Instructor\n\n"
        "Week(s): 3\n\n"
        "Day(s): Monday, Wednesday, Friday\n\n"
        "Timeslot(s):\n0600 - 0700\n\n"
        "Class Name Filter: RIDE\n"
    )

    query_str = sample_query_data.get_query_str(
        include_studio=True,
        include_instructors=True,
        include_weeks=True,
        include_days=True,
        include_time=True,
        include_class_name_filter=True,
    )
    assert query_str == query_expected_output
