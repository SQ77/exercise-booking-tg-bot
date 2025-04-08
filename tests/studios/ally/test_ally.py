"""
test_ally.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Ally.
"""
import logging
import pytest
import requests
from bs4 import BeautifulSoup
from common.studio_location import StudioLocation
from datetime import date
from studios.ally.ally import send_get_schedule_request, get_schedule_from_response_soup, get_instructorid_map_from_response_soup, get_ally_schedule_and_instructorid_map
from tests.studios.ally import expected_results

def test_send_get_schedule_request_single_location(mocker):
  """
  Test send_get_schedule_request flow.

  Args:
    - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
  """
  # Setup mocks
  mock_get = mocker.patch("requests.get", return_value=mocker.MagicMock(spec=requests.models.Response))
  mock_get.return_value.status_code = 200

  # Call the function to test
  week = 1
  response = send_get_schedule_request(week)

  # Assert that flow was called with the expected arguments
  mock_get.assert_called_once_with(
    url="https://ally.zingfit.com/reserve/index.cfm?action=Reserve.chooseClass",
    params={"wk": week, "site": 1}
  )
  assert response.status_code == 200

def test_get_schedule_from_response_soup(mocker, load_html):
  """
  Test get_schedule_from_response_soup flow.

  Args:
    - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
    - load_html (Callable[[str], str]): Fixture that loads HTML fixture content from the example_html_responses folder.
  """
  # Setup mocks
  mock_logger = logging.getLogger("test_logger")

  mock_soup = BeautifulSoup(load_html("crossstreet_7_to_13_apr.html"), "html.parser")

  # Call the function to test
  result = get_schedule_from_response_soup(mock_logger, mock_soup)

  # Assert that the response is as expected
  assert isinstance(result, dict)
  assert result.keys() == expected_results.EXPECTED_SCHEDULE.keys()
  for key in result:
    assert (result[key] == expected_results.EXPECTED_SCHEDULE[key]), (
      f"Expected result list {expected_results.EXPECTED_SCHEDULE[key]} "
      f"does not match actual result list {result[key]}."
    )

def test_get_instructorid_map_from_response_soup(mocker, load_html):
  """
  Test get_instructorid_map_from_response_soup flow.

  Args:
    - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
    - load_html (Callable[[str], str]): Fixture that loads HTML fixture content from the example_html_responses folder.
  """
  # Setup mocks
  mock_logger = logging.getLogger("test_logger")

  mock_soup = BeautifulSoup(load_html("crossstreet_7_to_13_apr.html"), "html.parser")

  # Call the function to test
  instructorid_map = get_instructorid_map_from_response_soup(mock_logger, mock_soup)

  # Assert that the response is as expected
  assert instructorid_map == expected_results.EXPECTED_INSTRUCTORID_MAP
