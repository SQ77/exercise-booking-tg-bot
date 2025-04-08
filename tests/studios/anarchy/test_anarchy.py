"""
test_anarchy.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Anarchy.
"""
import logging
import pytest
import requests
from bs4 import BeautifulSoup
from common.result_data import ResultData
from datetime import date
from studios.anarchy.anarchy import (
  get_anarchy_schedule_and_instructorid_map,
  get_instructorid_map_from_response_soup,
  get_schedule_from_response_soup,
  get_soup_from_response,
  send_get_schedule_request,
)
from tests.studios.anarchy import expected_results

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
  start_date = date(2025, 4, 8)
  end_date = date(2025, 4, 29)
  response = send_get_schedule_request(start_date, end_date)

  # Assert that flow was called with the expected arguments
  mock_get.assert_called_once_with(
    url = "https://widgets.mindbodyonline.com/widgets/schedules/189924/load_markup",
    params = {
      "callback": "jQuery36403516351979316319_1742526275618",
      "options[start_date]": start_date.strftime("%Y-%m-%d"),
      "options[end_date]": end_date.strftime("%Y-%m-%d"),
    },
  )
  assert response.status_code == 200

def test_get_soup_from_response_valid_jsonp(mocker, load_response_file):
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

  # Call the function to test
  soup = get_soup_from_response(mock_logger, mock_response)

  # Assert that the response is as expected
  assert isinstance(soup, BeautifulSoup)

def test_get_soup_from_response_invalid_jsonp(mocker):
  """
  Test get_schedule_from_response_soup flow.

  Args:
    - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
  """
  # Setup mocks
  mock_logger = mocker.Mock(spec=logging.Logger)

  mock_response = mocker.Mock(spec=requests.models.Response)
  mock_response.text = "<html><body>Non-JSONP content</body></html>"

  # Call the function to test
  soup = get_soup_from_response(mock_logger, mock_response)

  # Assert that the response is as expected
  assert soup is None
  mock_logger.warning.assert_called_once_with(f"Failed to parse response {mock_response.text}")

def test_get_schedule_from_response_soup(mocker, load_response_file):
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
  soup = get_soup_from_response(mock_logger, mock_response)
  assert isinstance(soup, BeautifulSoup)

  # Call the function to test
  result = get_schedule_from_response_soup(mock_logger, soup)

  # Assert that the response is as expected
  assert isinstance(result, dict)
  assert result.keys() == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE.keys()
  for key in result:
    assert (result[key] == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE[key]), (
      f"Expected result list {expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE[key]} "
      f"does not match actual result list {result[key]}."
    )

def test_get_instructorid_map_from_response_soup(mocker, load_response_file):
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
  soup = get_soup_from_response(mock_logger, mock_response)
  assert isinstance(soup, BeautifulSoup)

  # Call the function to test
  instructorid_map = get_instructorid_map_from_response_soup(mock_logger, soup)

  # Assert that the response is as expected
  assert instructorid_map == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_INSTRUCTORID_MAP

def test_get_anarchy_schedule_and_instructorid_map(mocker, load_response_file):
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
  schedule, instructorid_map = get_anarchy_schedule_and_instructorid_map(mock_logger)

  # Assert that the response is as expected
  assert isinstance(schedule, ResultData)
  assert isinstance(schedule.classes, dict)
  assert schedule.classes.keys() == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE.keys()
  for key in schedule.classes:
    assert (schedule.classes[key] == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE[key]), (
      f"Expected result list {expected_results.EXPECTED_ROBINSON_8_TO_28_APR_SCHEDULE[key]} "
      f"does not match actual result list {schedule.classes[key]}."
    )
  assert instructorid_map == expected_results.EXPECTED_ROBINSON_8_TO_28_APR_INSTRUCTORID_MAP
