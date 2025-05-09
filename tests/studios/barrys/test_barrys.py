"""
test_barrys.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Barrys.
"""

import logging
from datetime import date
from typing import Callable, NamedTuple

import pytest
import pytest_mock
from bs4 import BeautifulSoup

from common.capacity_info import CapacityInfo
from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from studios.barrys.barrys import (
    get_barrys_schedule_and_instructorid_map,
    get_instructorid_map_from_response_soup,
    get_schedule_from_response_soup,
    send_get_schedule_request,
)
from tests.conftest import is_classes_dict_equal
from tests.studios.barrys import expected_results


def test_send_get_schedule_request(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200

    # Call the function to test
    week = 0
    response = send_get_schedule_request(week)

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://apac.barrysbootcamp.com.au/reserve/index.cfm",
        params={"wk": week, "site": 1, "site2": 12, "action": "Reserve.chooseClass"},
    )
    assert response.status_code == 200


def test_get_schedule_from_response_soup(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_schedule_from_response_soup flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file("raffles_and_orchard_7_to_13_apr.html"), "html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(logger=mock_logger, soup=mock_soup)

    # Assert that the response is as expected
    assert is_classes_dict_equal(
        expected=expected_results.EXPECTED_RAFFLES_AND_ORCHARD_7_TO_13_APR_SCHEDULE,
        actual=result,
    )


class GetScheduleFromResponseSoupInvalidSoupArgs(NamedTuple):
    response_file_name: str
    expected_warning_substrs: list[str]
    expected_result: dict[date, ClassData]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetScheduleFromResponseSoupInvalidSoupArgs(
                response_file_name="invalid_schedule_missing_reservelist.html",
                expected_warning_substrs=["Failed to get schedule - Reserve list not found: "],
                expected_result={},
            ),
            id="Missing reserve list",
        ),
        pytest.param(
            GetScheduleFromResponseSoupInvalidSoupArgs(
                response_file_name="invalid_schedule_missing_data.html",
                expected_warning_substrs=[
                    "Failed to get schedule of day - ID not found: ",
                    "Failed to get session name: ",
                    "Failed to get session instructor: ",
                    "Failed to get session instructor name: ",
                    "Failed to get session time: ",
                    "Failed to get session location: ",
                    "Failed to get session studio location for 'New Location' - ",
                    "Found duplicate class ",
                ],
                expected_result={
                    date(2025, 4, 8): [
                        ClassData(
                            studio=StudioType.Barrys,
                            location=StudioLocation.Unknown,
                            name="Arms & Abs",
                            instructor="Ambika Chanrai",
                            time="10:05 AM",
                            availability=ClassAvailability.Available,
                            capacity_info=CapacityInfo(),
                        ),
                        ClassData(
                            studio=StudioType.Barrys,
                            location=StudioLocation.Raffles,
                            name="Arms & Abs",
                            instructor="Mandalyn Tan",
                            time="11:15 AM",
                            availability=ClassAvailability.Available,
                            capacity_info=CapacityInfo(),
                        ),
                    ]
                },
            ),
            id="Schedule missing day id/class name/instructor/instructor name/time/room",
        ),
    ],
)
def test_get_schedule_from_response_soup_invalid_soup(
    mocker: pytest_mock.plugin.MockerFixture,
    load_response_file: Callable[[str], str],
    args: GetScheduleFromResponseSoupInvalidSoupArgs,
) -> None:
    """
    Test get_schedule_from_response_soup with invalid soup flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.
      - args (GetScheduleFromResponseSoupInvalidSoupArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file(args.response_file_name), "html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(logger=mock_logger, soup=mock_soup)

    # Assert that the response is as expected
    assert is_classes_dict_equal(expected=args.expected_result, actual=result)

    # Assert that flow was called with the expected arguments
    assert mock_logger.warning.call_count == len(args.expected_warning_substrs)
    for expected_warning_substr in args.expected_warning_substrs:
        assert any(expected_warning_substr in str(call_args[0][0]) for call_args in mock_logger.warning.call_args_list)


def test_get_instructorid_map_from_response_soup(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_instructorid_map_from_response_soup flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file("raffles_and_orchard_7_to_13_apr.html"), "html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(logger=mock_logger, soup=mock_soup)

    # Assert that the response is as expected
    assert instructorid_map == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_7_TO_13_APR_INSTRUCTORID_MAP


@pytest.mark.parametrize(
    ("response_file_name", "expected_warning_substrs"),
    [
        pytest.param(
            "invalid_instructors_missing_reserve_filter.html",
            ["Failed to get list of instructors - Reserve filter not found: "],
            id="Missing reserve filter",
        ),
        pytest.param(
            "invalid_instructors_missing_reserve_filter_1.html",
            ["Failed to get list of instructors - Instructor filter not found: "],
            id="Missing reserve filter 1",
        ),
        pytest.param(
            "invalid_instructors_missing_data.html",
            [
                "Failed to get id of instructor ambika chanrai - A tag is null: ",
                "Failed to get id of instructor gino morales - Href is null: ",
                "Failed to get id of instructor ian chan - Regex failed to match: ",
            ],
            id="Instructors missing or invalid 'a' tag/href/regex",
        ),
    ],
)
def test_get_instructorid_map_from_response_soup_invalid_soup(
    mocker: pytest_mock.plugin.MockerFixture,
    load_response_file: Callable[[str], str],
    response_file_name: str,
    expected_warning_substrs: list[str],
) -> None:
    """
    Test get_instructorid_map_from_response_soup with invalid soup flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.
      - response_file_name (str): Name of response file to use for the test.
      - expected_warning_substrs (list[str]):
        List of expected warning messages to be logged. Does not include dump of soup.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file(response_file_name), "html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(logger=mock_logger, soup=mock_soup)

    # Assert that the response is as expected
    assert instructorid_map == {}

    # Assert that flow was called with the expected arguments
    assert mock_logger.warning.call_count == len(expected_warning_substrs)
    for expected_warning_substr in expected_warning_substrs:
        assert any(expected_warning_substr in str(call_args[0][0]) for call_args in mock_logger.warning.call_args_list)


def test_get_barrys_schedule_and_instructorid_map(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_barrys_schedule_and_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_week_0_request_response = mocker.Mock()
    mock_week_0_request_response.text = load_response_file("raffles_and_orchard_8_to_14_apr.html")

    mock_week_1_request_response = mocker.Mock()
    mock_week_1_request_response.text = load_response_file("raffles_and_orchard_15_to_21_apr.html")

    mock_week_2_request_response = mocker.Mock()
    mock_week_2_request_response.text = load_response_file("raffles_and_orchard_22_to_28_apr.html")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_week_0_request_response,
            mock_week_1_request_response,
            mock_week_2_request_response,
        ],
    )

    # Call the function to test
    schedule, instructorid_map = get_barrys_schedule_and_instructorid_map(mock_logger)

    # Assert that the response is as expected
    assert is_classes_dict_equal(
        expected=expected_results.EXPECTED_RAFFLES_AND_ORCHARD_8_TO_28_APR_SCHEDULE,
        actual=schedule.classes,
    )
    assert instructorid_map == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_2_TO_28_APR_INSTRUCTORID_MAP
