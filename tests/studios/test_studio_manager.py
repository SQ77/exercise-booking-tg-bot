"""
test_studio_manager.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the StudioManager class.
"""

from datetime import date
from functools import partial

import pytest_mock
from readerwriterlock.rwlock import RWLockFair

from common.class_data import ClassData
from common.result_data import ResultData
from studios.studio_manager import StudioManager
from tests.conftest import is_classes_dict_equal


def test_init(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test initialization of StudioManager object.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get_schedule_and_instructorid_map_func = mocker.Mock()

    # Create ResultData object
    studio_manager = StudioManager(get_schedule_and_instructorid_map_func=mock_get_schedule_and_instructorid_map_func)

    # Assert that the object is created as expected
    assert studio_manager.instructorid_map == {}
    assert isinstance(studio_manager.instructorid_map_lock, RWLockFair)
    assert studio_manager.instructor_names == []
    assert isinstance(studio_manager.instructor_names_lock, RWLockFair)
    assert isinstance(studio_manager.get_schedule_and_instructorid_map_func, partial)


def test_get_schedule(
    mocker: pytest_mock.MockerFixture,
    sample_classes_dict: dict[date, list[ClassData]],
) -> None:
    """
    Test get_schedule flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_classes_dict (dict[date, list[ClassData]]): Sample dictionary of dates and details of classes.

    """
    test_schedule = ResultData(classes=sample_classes_dict)
    test_instructorid_map = {
        "Instructor 1": "111",
        "Instructor 2": "222",
        "Instructor 3": "333",
    }
    test_instructor_names = [instructor.lower() for instructor in list(test_instructorid_map)]

    # Setup mocks
    mock_get_schedule_and_instructorid_map_func = mocker.Mock()
    mock_get_schedule_and_instructorid_map_func.return_value = (test_schedule, test_instructorid_map)

    # Create ResultData object
    studio_manager = StudioManager(get_schedule_and_instructorid_map_func=mock_get_schedule_and_instructorid_map_func)

    # Call the function to test
    schedule = studio_manager.get_schedule()

    # Assert that flow was called with the expected arguments
    mock_get_schedule_and_instructorid_map_func.assert_called_once_with()

    # Assert that the response is as expected
    assert is_classes_dict_equal(expected=test_schedule.classes, actual=schedule.classes)
    assert studio_manager.get_instructorid_map() == test_instructorid_map
    assert studio_manager.get_instructor_names() == test_instructor_names
