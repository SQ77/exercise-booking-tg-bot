"""
test_anarchy.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Anarchy.
"""

import logging
from datetime import date
from typing import Callable

import pytest_mock
import requests
from bs4 import BeautifulSoup

from studios.anarchy.anarchy import (
    get_anarchy_schedule_and_instructorid_map,
    get_instructorid_map_from_response_soup,
    get_schedule_from_response_soup,
    get_soup_from_response,
    send_get_schedule_request,
)
from tests.conftest import is_classes_dict_equal
from tests.studios.anarchy import expected_results


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
    start_date = date(2025, 4, 8)
    end_date = date(2025, 4, 29)
    response = send_get_schedule_request(start_date, end_date)

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgets.mindbodyonline.com/widgets/schedules/189924/load_markup",
        params={
            "callback": "jQuery36403516351979316319_1742526275618",
            "options[start_date]": start_date.strftime("%Y-%m-%d"),
            "options[end_date]": end_date.strftime("%Y-%m-%d"),
        },
    )

    # Assert that the response is as expected
    assert response.status_code == 200


def test_get_soup_from_response_valid_json(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_soup_from_response flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.text = load_response_file("robinson_8_to_28_apr.txt")

    # Call the function to test
    soup = get_soup_from_response(logger=mock_logger, response=mock_response)

    # Assert that the response is as expected
    assert isinstance(soup, BeautifulSoup)


def test_get_soup_from_response_match_regex_error(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_soup_from_response response does not match regex flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.text = "<html><body>Non-JSONP content</body></html>"

    # Call the function to test
    soup = get_soup_from_response(logger=mock_logger, response=mock_response)

    # Assert that flow was called with the expected arguments
    mock_logger.warning.assert_called_once_with(f"Failed to parse response {mock_response.text}")

    # Assert that the response is as expected
    assert soup is None


def test_get_soup_from_response_parse_json_error(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_soup_from_response response matches regex but is invalid json flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.text = "myFunction('//s);"

    # Call the function to test
    soup = get_soup_from_response(logger=mock_logger, response=mock_response)

    # Assert that flow was called with the expected arguments
    mock_logger.warning.assert_called_once_with(
        f"Failed to parse response to json {mock_response.text} - Expecting value: line 1 column 1 (char 0)"
    )

    # Assert that the response is as expected
    assert soup is None


def test_get_soup_from_response_read_json_error(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_soup_from_response json missing class_sessions field flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.text = 'myFunction({"no_class_session":123});'

    # Call the function to test
    soup = get_soup_from_response(logger=mock_logger, response=mock_response)

    # Assert that flow was called with the expected arguments
    mock_logger.warning.assert_called_once_with(
        "Failed to parse html from response {'no_class_session': 123} - 'class_sessions'"
    )

    # Assert that the response is as expected
    assert soup is None


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

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.text = load_response_file("robinson_8_to_28_apr.txt")

    # Get soup to test function with
    soup = get_soup_from_response(logger=mock_logger, response=mock_response)
    assert isinstance(soup, BeautifulSoup)

    # Call the function to test
    result = get_schedule_from_response_soup(mock_logger, soup)

    # Assert that the response is as expected
    assert is_classes_dict_equal(
        expected=expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE,
        actual=result,
    )


def test_get_schedule_from_response_soup_invalid_soup(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_schedule_from_response_soup with invalid soup flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    # Get soup to test function with
    soup = BeautifulSoup(markup=load_response_file("invalid_schedule.html"), features="html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(mock_logger, soup)

    # Assert that flow was called with the expected arguments
    assert mock_logger.warning.call_count == 5

    # Assert that the response is as expected
    assert is_classes_dict_equal(expected={}, actual=result)


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

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.text = load_response_file("robinson_8_to_28_apr.txt")

    # Get soup to test function with
    soup = get_soup_from_response(logger=mock_logger, response=mock_response)
    assert isinstance(soup, BeautifulSoup)

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(logger=mock_logger, soup=soup)

    # Assert that the response is as expected
    assert instructorid_map == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_INSTRUCTORID_MAP


def test_get_instructorid_map_from_response_soup_invalid_soup(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_instructorid_map_from_response_soup with invalid soup flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)
    soup = BeautifulSoup(markup=load_response_file("invalid_instructors.html"), features="html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(logger=mock_logger, soup=soup)

    # Assert that the response is as expected
    assert instructorid_map == {}


def test_get_anarchy_schedule_and_instructorid_map(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_anarchy_schedule_and_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_request_response = mocker.Mock()
    mock_request_response.text = load_response_file("robinson_8_to_28_apr.txt")

    mocker.patch("requests.get", side_effect=[mock_request_response])

    # Call the function to test
    schedule, instructorid_map = get_anarchy_schedule_and_instructorid_map(logger=mock_logger)

    # Assert that the response is as expected
    assert is_classes_dict_equal(
        expected=expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE,
        actual=schedule.classes,
    )
    assert instructorid_map == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_INSTRUCTORID_MAP


def test_get_anarchy_schedule_and_instructorid_map_end_of_day(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_anarchy_schedule_and_instructorid_map no more classes on current day flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_request_response_1 = mocker.Mock()
    mock_request_response_1.text = load_response_file("robinson_no_classes.txt")

    mock_request_response_2 = mocker.Mock()
    mock_request_response_2.text = load_response_file("robinson_8_to_28_apr.txt")

    mocker.patch("requests.get", side_effect=[mock_request_response_1, mock_request_response_2])

    # Call the function to test
    schedule, instructorid_map = get_anarchy_schedule_and_instructorid_map(logger=mock_logger)

    # Assert that the response is as expected
    assert is_classes_dict_equal(
        expected=expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE,
        actual=schedule.classes,
    )
    assert instructorid_map == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_INSTRUCTORID_MAP


def test_get_anarchy_schedule_and_instructorid_map_empty_soup(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_anarchy_schedule_and_instructorid_map soup is none flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_request_response = mocker.Mock()
    mock_request_response.text = ""

    mocker.patch("requests.get", side_effect=[mock_request_response])

    # Call the function to test
    schedule, instructorid_map = get_anarchy_schedule_and_instructorid_map(logger=mock_logger)

    # Assert that the response is as expected
    assert is_classes_dict_equal(expected={}, actual=schedule.classes)
    assert instructorid_map == {}
