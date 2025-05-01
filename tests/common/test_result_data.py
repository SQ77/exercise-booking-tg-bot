"""
test_result_data.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the ResultData class.
"""

from datetime import date, datetime
from typing import NamedTuple

import pytest
import pytest_mock

from common.capacity_info import CapacityInfo
from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.query_data import QueryData
from common.result_data import ResultData
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from tests.conftest import is_classes_dict_equal


def test_init_default_arguments() -> None:
    """
    Test initialization of ResultData object with the default argument.
    """
    # Create ResultData object
    result_data = ResultData()

    # Assert that the object is created as expected
    assert result_data.classes == {}


def test_init(sample_class_data: ClassData) -> None:
    """
    Test initialization of ResultData object with the classes dict.

    Args:
      - sample_class_data (ClassData): Sample ClassData object for the test.

    """
    test_classes = {date(2025, 4, 20): [sample_class_data]}

    # Create ResultData object
    result_data = ResultData(classes=test_classes)

    # Assert that the object is created as expected
    assert result_data.classes == test_classes


def test_add_classes(sample_class_data: ClassData) -> None:
    """
    Test add_classes flow.

    Args:
      - sample_class_data (ClassData): Sample ClassData object for the test.

    """
    test_classes = {date(2025, 4, 20): [sample_class_data]}
    test_classes_to_add = {
        date(2025, 4, 20): [
            ClassData(
                studio=StudioType.AllySpin,
                location=StudioLocation.Maxwell,
                name="RIDE: ESSENTIALS 50",
                instructor="Ally Instructor",
                time="1:00 PM",
                availability=ClassAvailability.Available,
                capacity_info=CapacityInfo(),
            ),
        ],
        date(2025, 4, 21): [
            ClassData(
                studio=StudioType.AbsolutePilates,
                location=StudioLocation.Raffles,
                name="PILATES (Reformer) Fit & Tone 60 - Rm2",
                instructor="Absolute Instructor",
                time="9:00 AM",
                availability=ClassAvailability.Available,
                capacity_info=CapacityInfo(),
            ),
        ],
    }
    expected_classes = {
        date(2025, 4, 20): [
            sample_class_data,
            ClassData(
                studio=StudioType.AllySpin,
                location=StudioLocation.Maxwell,
                name="RIDE: ESSENTIALS 50",
                instructor="Ally Instructor",
                time="1:00 PM",
                availability=ClassAvailability.Available,
                capacity_info=CapacityInfo(),
            ),
        ],
        date(2025, 4, 21): [
            ClassData(
                studio=StudioType.AbsolutePilates,
                location=StudioLocation.Raffles,
                name="PILATES (Reformer) Fit & Tone 60 - Rm2",
                instructor="Absolute Instructor",
                time="9:00 AM",
                availability=ClassAvailability.Available,
                capacity_info=CapacityInfo(),
            ),
        ],
    }

    # Create ResultData object
    result_data = ResultData(classes=test_classes)

    # Call the function to test
    result_data.add_classes(classes=test_classes_to_add)

    # Assert that the object is created as expected
    assert result_data.classes == expected_classes


def test_add_classes_none() -> None:
    """
    Test add_classes input classes is none flow.
    """

    # Create ResultData object
    result_data = ResultData(classes=None)

    # Call the function to test
    result_data.add_classes(classes=None)

    # Assert that the object is created as expected
    assert result_data.classes == {}


def test_add_classes_to_empty_result_data(sample_class_data: ClassData) -> None:
    """
    Test add_classes flow.

    Args:
      - sample_class_data (ClassData): Sample ClassData object for the test.

    """
    test_classes_to_add = {
        date(2025, 4, 20): [sample_class_data],
        date(2025, 4, 21): [
            ClassData(
                studio=StudioType.Barrys,
                location=StudioLocation.Orchard,
                name="Arms & Abs",
                instructor="Barrys Instructor",
                time="6:00 PM",
                availability=ClassAvailability.Waitlist,
                capacity_info=CapacityInfo(),
            ),
        ],
    }
    expected_classes = {
        date(2025, 4, 20): [sample_class_data],
        date(2025, 4, 21): [
            ClassData(
                studio=StudioType.Barrys,
                location=StudioLocation.Orchard,
                name="Arms & Abs",
                instructor="Barrys Instructor",
                time="6:00 PM",
                availability=ClassAvailability.Waitlist,
                capacity_info=CapacityInfo(),
            ),
        ],
    }

    # Create ResultData object
    result_data = ResultData(classes=None)

    # Call the function to test
    result_data.add_classes(classes=test_classes_to_add)

    # Assert that the object is created as expected
    assert result_data.classes == expected_classes


class GetDataArgs(NamedTuple):
    query: QueryData
    expected_classes: dict[date, ClassData]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetDataArgs(
                query=QueryData(
                    studios={
                        StudioType.Barrys: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        )
                    },
                    current_studio=StudioType.Barrys,
                    weeks=1,
                    days=["Monday", "Sunday"],
                    start_times=[],
                    class_name_filter="",
                ),
                expected_classes={
                    date(2025, 4, 21): [
                        ClassData(
                            studio=StudioType.Barrys,
                            location=StudioLocation.Orchard,
                            name="Arms & Abs",
                            instructor="Barrys Instructor",
                            time="10:00 AM",
                            availability=ClassAvailability.Waitlist,
                            capacity_info=CapacityInfo(
                                has_info=True,
                                capacity=40,
                                remaining=0,
                                waitlist_capacity=20,
                                waitlist_reserved=18,
                            ),
                        ),
                    ],
                },
            ),
            id="Filter out classes that have already ended",
        ),
        pytest.param(
            GetDataArgs(
                query=QueryData(
                    studios={
                        StudioType.Rev: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        )
                    },
                    current_studio=StudioType.Rev,
                    weeks=1,
                    days=["All"],
                    start_times=[],
                    class_name_filter="",
                ),
                expected_classes={
                    date(2025, 4, 21): [
                        ClassData(
                            studio=StudioType.Rev,
                            location=StudioLocation.TJPG,
                            name="Ride",
                            instructor="Rev Instructor",
                            time="12:00 PM",
                            availability=ClassAvailability.Available,
                            capacity_info=CapacityInfo(
                                has_info=True,
                                capacity=40,
                                remaining=16,
                                waitlist_capacity=20,
                                waitlist_reserved=0,
                            ),
                        ),
                    ],
                },
            ),
            id="Filter out classes by studio and weeks",
        ),
        pytest.param(
            GetDataArgs(
                query=QueryData(
                    studios={
                        StudioType.Rev: StudioData(
                            locations=[StudioLocation.Orchard],
                            instructors=["All"],
                        )
                    },
                    current_studio=StudioType.Rev,
                    weeks=1,
                    days=["All"],
                    start_times=[],
                    class_name_filter="",
                ),
                expected_classes={},
            ),
            id="Filter out classes by location",
        ),
        pytest.param(
            GetDataArgs(
                query=QueryData(
                    studios={
                        StudioType.AllySpin: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["Ally Instructor"],
                        )
                    },
                    current_studio=StudioType.AllySpin,
                    weeks=3,
                    days=["All"],
                    start_times=[],
                    class_name_filter="",
                ),
                expected_classes={
                    date(2025, 5, 6): [
                        ClassData(
                            studio=StudioType.AllySpin,
                            location=StudioLocation.Maxwell,
                            name="Essentials 50",
                            instructor="Ally Instructor",
                            time="10:00 AM",
                            availability=ClassAvailability.Available,
                            capacity_info=CapacityInfo(),
                        ),
                    ],
                },
            ),
            id="Filter out class by instructor name",
        ),
        pytest.param(
            GetDataArgs(
                query=QueryData(
                    studios={
                        StudioType.AllySpin: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        )
                    },
                    current_studio=StudioType.AllySpin,
                    weeks=3,
                    days=["All"],
                    start_times=[(datetime.strptime("07:00", "%H:%M"), datetime.strptime("09:00", "%H:%M"))],
                    class_name_filter="",
                ),
                expected_classes={
                    date(2025, 5, 6): [
                        ClassData(
                            studio=StudioType.AllySpin,
                            location=StudioLocation.CrossStreet,
                            name="Essentials 50",
                            instructor="Test",
                            time="8:00 AM",
                            availability=ClassAvailability.Available,
                            capacity_info=CapacityInfo(),
                        ),
                    ],
                },
            ),
            id="Filter out class by time filter",
        ),
        pytest.param(
            GetDataArgs(
                query=QueryData(
                    studios={
                        StudioType.Barrys: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        )
                    },
                    current_studio=StudioType.Barrys,
                    weeks=1,
                    days=["All"],
                    start_times=[],
                    class_name_filter="arms",
                ),
                expected_classes={
                    date(2025, 4, 21): [
                        ClassData(
                            studio=StudioType.Barrys,
                            location=StudioLocation.Orchard,
                            name="Arms & Abs",
                            instructor="Barrys Instructor",
                            time="10:00 AM",
                            availability=ClassAvailability.Waitlist,
                            capacity_info=CapacityInfo(
                                has_info=True,
                                capacity=40,
                                remaining=0,
                                waitlist_capacity=20,
                                waitlist_reserved=18,
                            ),
                        ),
                    ],
                },
            ),
            id="Filter out class by class name filter",
        ),
    ],
)
def test_get_data(
    mocker: pytest_mock.plugin.MockerFixture,
    sample_classes_dict: dict[date, list[ClassData]],
    args: GetDataArgs,
) -> None:
    """
    Test get_data flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_classes_dict (dict[date, list[ClassData]]): Sample dictionary of dates and details of classes.
      - args (GetDataArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_datetime = mocker.patch("common.result_data.datetime", wraps=datetime)
    mock_datetime.now.return_value = datetime(2025, 4, 20, 13, 0, 0)

    # Create ResultData object
    result_data = ResultData(classes=sample_classes_dict)

    # Call the function to test
    result = result_data.get_data(query=args.query)

    # Assert that the object is created as expected
    assert is_classes_dict_equal(expected=args.expected_classes, actual=result.classes)


def test_get_data_classes_is_empty(sample_empty_query_data: QueryData) -> None:
    """
    Test get_data when classes is empty flow.

    Args:
      - sample_empty_query_data (QueryData): Sample QueryData object for the test.

    """
    # Create ResultData object
    result_data = ResultData(classes=None)

    # Call the function to test
    result = result_data.get_data(query=sample_empty_query_data)

    # Assert that the object is created as expected
    assert result.classes == {}


def test_get_result_str(sample_classes_dict: dict[date, list[ClassData]]) -> None:
    """
    Test get_result_str flow.

    Args:
      - sample_classes_dict (dict[date, list[ClassData]]): Sample dictionary of dates and details of classes.

    """
    expected_result_str = (
        "*Sunday, 20 April*\n"
        "*10:00 AM* - Chest, Back, Abs @ Raffles (Barrys Instructor)\n"
        "\n"
        "*Monday, 21 April*\n"
        "*[W] 10:00 AM* - Arms & Abs @ Orchard (Barrys Instructor) - 18 Member(s) on Waitlist\n"
        "*12:00 PM* - Ride @ TJPG (Rev Instructor) - 16 Spot(s) Remaining\n"
        "\n"
        "*Tuesday, 22 April*\n"
        "*[F] 5:00 PM* - Reformer @ Great World (Absolute Instructor)\n"
        "\n"
        "*Wednesday, 23 April*\n"
        "*[Cancelled] 1:00 PM* - Open Gym @ Robinson (Anarchy Instructor)\n"
        "\n"
        "*Thursday, 24 April*\n"
        "*7:00 PM* - Essentials 60 (Absolute Instructor)\n"
        "\n"
        "*Tuesday, 06 May*\n"
        "*8:00 AM* - Essentials 50 @ Cross Street (Test)\n"
        "*10:00 AM* - Essentials 50 @ Maxwell (Ally Instructor)\n"
        "\n"
        "*Wednesday, 07 May*\n"
        "*[F] 6:45 PM* - Ride @ TJPG (Rev Instructor) - 0 Spot(s) Remaining\n"
        "\n"
    )

    # Create ResultData object
    result_data = ResultData(classes=sample_classes_dict)

    # Call the function to test
    result_str = result_data.get_result_str()

    # Assert that the object is created as expected
    assert result_str == expected_result_str


def test_get_result_str_no_classes() -> None:
    """
    Test get_result_str flow.

    Args:
      - sample_classes_dict (dict[date, list[ClassData]]): Sample dictionary of dates and details of classes.

    """
    # Create ResultData object
    result_data = ResultData(classes=None)

    # Call the function to test
    result_str = result_data.get_result_str()

    # Assert that the object is created as expected
    assert result_str == "No classes found"
