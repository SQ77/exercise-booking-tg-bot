"""
test_barrys.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Barrys.
"""

import logging
from typing import Callable

import pytest_mock
import requests
from bs4 import BeautifulSoup

from common.result_data import ResultData
from studios.barrys.barrys import (
    get_barrys_schedule_and_instructorid_map,
    get_instructorid_map_from_response_soup,
    get_schedule_from_response_soup,
    send_get_schedule_request,
)
from tests.studios.barrys import expected_results


def test_send_get_schedule_request(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get", return_value=mocker.MagicMock(spec=requests.models.Response))
    mock_get.return_value.status_code = 200

    # Call the function to test
    week = 0
    response = send_get_schedule_request(week)

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://apac.barrysbootcamp.com.au/reserve/index.cfm?action=Reserve.chooseClass",
        params={"wk": week, "site": 1, "site2": 12},
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
    result = get_schedule_from_response_soup(mock_logger, mock_soup)

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_7_TO_13_APR_SCHEDULE.keys()
    for key in result:
        assert result[key] == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_7_TO_13_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_RAFFLES_AND_ORCHARD_7_TO_13_APR_SCHEDULE[key]} "
            f"does not match actual result list {result[key]}."
        )


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
    instructorid_map = get_instructorid_map_from_response_soup(mock_logger, mock_soup)

    # Assert that the response is as expected
    assert instructorid_map == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_7_TO_13_APR_INSTRUCTORID_MAP


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
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_8_TO_28_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_8_TO_28_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_RAFFLES_AND_ORCHARD_8_TO_28_APR_SCHEDULE[key]} "
            f"does not match actual result list {schedule.classes[key]}."
        )
    assert instructorid_map == expected_results.EXPECTED_RAFFLES_AND_ORCHARD_2_TO_28_APR_INSTRUCTORID_MAP
