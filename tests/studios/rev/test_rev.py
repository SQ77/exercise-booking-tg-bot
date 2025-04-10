"""
test_rev.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Rev.
"""

import logging
from datetime import date

import requests

from common.result_data import ResultData
from common.studio_location import StudioLocation
from studios.rev.data import SITE_ID_MAP
from studios.rev.rev import (
    get_instructorid_map,
    get_rev_schedule,
    get_rev_schedule_and_instructorid_map,
    parse_get_schedule_response,
    send_get_schedule_request,
)
from tests.studios.rev import expected_results


def test_send_get_schedule_request(mocker):
    """
    Test send_get_schedule_request flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get", return_value=mocker.MagicMock(spec=requests.models.Response))
    mock_get.return_value.status_code = 200

    # Call the function to test
    location = StudioLocation.Bugis
    start_date = date(2025, 4, 8)
    end_date = date(2025, 4, 29)
    security_token = "test_security_token"
    response = send_get_schedule_request(location, start_date, end_date, security_token)

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/sessions?sessionCategory=classes",
        params={
            "siteID": SITE_ID_MAP[location],
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
        },
        headers={
            "Content-Type": "application/json",
            "Securitytoken": security_token,
        },
    )
    assert response.status_code == 200


def test_parse_get_schedule_response(mocker, load_response_file):
    """
    Test parse_get_schedule_response flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.status_code = 200
    mock_response.text = load_response_file("orchard_9_to_18_apr.json")

    # Call the function to test
    result = parse_get_schedule_response(mock_logger, mock_response)

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE.keys()
    for key in result:
        assert result[key] == expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE[key]} "
            f"does not match actual result list {result[key]}."
        )


def test_get_rev_schedule(mocker, load_response_file):
    """
    Test get_rev_schedule flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_bugis_schedule_request_response = mocker.Mock()
    mock_bugis_schedule_request_response.status_code = 200
    mock_bugis_schedule_request_response.text = load_response_file("bugis_10_to_12_apr.json")

    mock_orchard_schedule_request_response = mocker.Mock()
    mock_orchard_schedule_request_response.status_code = 200
    mock_orchard_schedule_request_response.text = load_response_file("orchard_10_to_12_apr.json")

    mock_tjpg_schedule_request_response = mocker.Mock()
    mock_tjpg_schedule_request_response.status_code = 200
    mock_tjpg_schedule_request_response.text = load_response_file("tjpg_10_to_12_apr.json")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_bugis_schedule_request_response,
            mock_orchard_schedule_request_response,
            mock_tjpg_schedule_request_response,
        ],
    )

    # Call the function to test
    schedule = get_rev_schedule(mock_logger, "test_security_token")

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key]} "
            f"does not match actual result list {schedule.classes[key]}."
        )


def test_get_instructorid_map(mocker, load_response_file):
    """
    Test get_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_bugis_instructors_request_response = mocker.Mock()
    mock_bugis_instructors_request_response.status_code = 200
    mock_bugis_instructors_request_response.text = load_response_file("bugis_instructors.json")

    mock_orchard_instructors_request_response = mocker.Mock()
    mock_orchard_instructors_request_response.status_code = 200
    mock_orchard_instructors_request_response.text = load_response_file("orchard_instructors.json")

    mock_tjpg_instructors_request_response = mocker.Mock()
    mock_tjpg_instructors_request_response.status_code = 200
    mock_tjpg_instructors_request_response.text = load_response_file("tjpg_instructors.json")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_bugis_instructors_request_response,
            mock_orchard_instructors_request_response,
            mock_tjpg_instructors_request_response,
        ],
    )

    # Call the function to test
    instructorid_map = get_instructorid_map(mock_logger, "test_security_token")

    # Assert that the response is as expected
    assert instructorid_map == expected_results.EXPECTED_BUGIS_10_TO_12_APR_INSTRUCTORID_MAP


def test_get_rev_schedule_and_instructorid_map(mocker, load_response_file):
    """
    Test get_rev_schedule_and_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_bugis_schedule_request_response = mocker.Mock()
    mock_bugis_schedule_request_response.status_code = 200
    mock_bugis_schedule_request_response.text = load_response_file("bugis_10_to_12_apr.json")

    mock_orchard_schedule_request_response = mocker.Mock()
    mock_orchard_schedule_request_response.status_code = 200
    mock_orchard_schedule_request_response.text = load_response_file("orchard_10_to_12_apr.json")

    mock_tjpg_schedule_request_response = mocker.Mock()
    mock_tjpg_schedule_request_response.status_code = 200
    mock_tjpg_schedule_request_response.text = load_response_file("tjpg_10_to_12_apr.json")

    mock_bugis_instructors_request_response = mocker.Mock()
    mock_bugis_instructors_request_response.status_code = 200
    mock_bugis_instructors_request_response.text = load_response_file("bugis_instructors.json")

    mock_orchard_instructors_request_response = mocker.Mock()
    mock_orchard_instructors_request_response.status_code = 200
    mock_orchard_instructors_request_response.text = load_response_file("orchard_instructors.json")

    mock_tjpg_instructors_request_response = mocker.Mock()
    mock_tjpg_instructors_request_response.status_code = 200
    mock_tjpg_instructors_request_response.text = load_response_file("tjpg_instructors.json")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_bugis_schedule_request_response,
            mock_orchard_schedule_request_response,
            mock_tjpg_schedule_request_response,
            mock_bugis_instructors_request_response,
            mock_orchard_instructors_request_response,
            mock_tjpg_instructors_request_response,
        ],
    )

    # Call the function to test
    schedule, instructorid_map = get_rev_schedule_and_instructorid_map(mock_logger, "test_security_token")

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key], (
            f"Expected result list {expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key]} "
            f"does not match actual result list {schedule.classes[key]}."
        )
    assert instructorid_map == expected_results.EXPECTED_BUGIS_10_TO_12_APR_INSTRUCTORID_MAP
