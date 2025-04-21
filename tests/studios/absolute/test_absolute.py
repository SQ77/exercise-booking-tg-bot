"""
test_absolute.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Absolute.
"""

import logging
from typing import Callable

import pytest_mock
import requests
from bs4 import BeautifulSoup

from common.result_data import ResultData
from common.studio_location import StudioLocation
from studios.absolute.absolute import (
    get_absolute_schedule_and_instructorid_map,
    get_instructorid_map_from_response_soup,
    get_schedule_from_response_soup,
    send_get_schedule_request,
)
from studios.absolute.data import LOCATION_MAP
from tests.studios.absolute import expected_results


def test_send_get_schedule_request_single_location(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow with a single location.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get", return_value=mocker.MagicMock(spec=requests.models.Response))
    mock_get.return_value.status_code = 200

    # Call the function to test
    locations = [StudioLocation.Centrepoint]
    week = 1
    response = send_get_schedule_request(locations, week)

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm",
        params={"wk": week, "site": LOCATION_MAP[locations[0]], "action": "Reserve.chooseClass"},
    )
    assert response.status_code == 200


def test_send_get_schedule_request_multiple_locations(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow with multiple locations.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get", return_value=mocker.MagicMock(spec=requests.models.Response))
    mock_get.return_value.status_code = 200

    # Call the function to test
    locations = [
        StudioLocation.Centrepoint,
        StudioLocation.StarVista,
        StudioLocation.MilleniaWalk,
        StudioLocation.i12,
        StudioLocation.GreatWorld,
    ]
    week = 2
    response = send_get_schedule_request(locations, week)

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm",
        params={
            "wk": week,
            "site": LOCATION_MAP[locations[0]],
            "site2": LOCATION_MAP[locations[1]],
            "site3": LOCATION_MAP[locations[2]],
            "site4": LOCATION_MAP[locations[3]],
            "site5": LOCATION_MAP[locations[4]],
            "action": "Reserve.chooseClass",
        },
    )
    assert response.status_code == 200


def test_get_schedule_from_response_soup_single_location(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_schedule_from_response_soup flow with a single location.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file("raffles_6_to_12_apr.html"), "html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(mock_logger, mock_soup)

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == expected_results.EXPECTED_RAFFLES_6_TO_12_APR_SCHEDULE.keys()
    for key in result:
        assert result[key] == expected_results.EXPECTED_RAFFLES_6_TO_12_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_RAFFLES_6_TO_12_APR_SCHEDULE[key]} "
            f"does not match actual result list {result[key]}."
        )


def test_get_schedule_from_response_soup_multiple_locations(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_schedule_from_response_soup flow with multiple locations.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file("milleniawalk_and_i12_7_to_12_apr.html"), "html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(mock_logger, mock_soup)

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == expected_results.EXPECTED_MW_AND_I12_7_TO_12_APR_SCHEDULE.keys()
    for key in result:
        assert result[key] == expected_results.EXPECTED_MW_AND_I12_7_TO_12_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_MW_AND_I12_7_TO_12_APR_SCHEDULE[key]} "
            f"does not match actual result list {result[key]}."
        )


def test_get_instructorid_map_from_response_soup_single_location(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_instructorid_map_from_response_soup flow with a single location.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file("raffles_6_to_12_apr.html"), "html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(mock_logger, mock_soup)

    # Assert that the response is as expected
    assert instructorid_map == expected_results.EXPECTED_RAFFLES_6_TO_12_APR_INSTRUCTORID_MAP


def test_get_instructorid_map_from_response_soup_multiple_locations(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_instructorid_map_from_response_soup flow with a multiple locations.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file("milleniawalk_and_i12_7_to_12_apr.html"), "html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(mock_logger, mock_soup)

    # Assert that the response is as expected
    assert instructorid_map == expected_results.EXPECTED_MW_AND_I12_7_TO_12_APR_INSTRUCTORID_MAP


def test_get_absolute_schedule_and_instructorid_map(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_absolute_schedule_and_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_week_0_first_request_response = mocker.Mock()
    mock_week_0_first_request_response.text = load_response_file("centrepoint_7_to_13_apr.html")

    mock_week_0_second_request_response = mocker.Mock()
    mock_week_0_second_request_response.text = load_response_file("greatworld_8_to_13_apr.html")

    mock_week_1_first_request_response = mocker.Mock()
    mock_week_1_first_request_response.text = load_response_file("centrepoint_14_to_20_apr.html")

    mock_week_1_second_request_response = mocker.Mock()
    mock_week_1_second_request_response.text = load_response_file("greatworld_14_to_20_apr.html")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_week_0_first_request_response,
            mock_week_0_second_request_response,
            mock_week_1_first_request_response,
            mock_week_1_second_request_response,
        ],
    )

    # Call the function to test
    schedule, instructorid_map = get_absolute_schedule_and_instructorid_map(mock_logger)

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_SCHEDULE[key]} "
            f"does not match actual result list {schedule.classes[key]}."
        )
    assert instructorid_map == expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_INSTRUCTORID_MAP
