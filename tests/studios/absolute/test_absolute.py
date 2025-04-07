"""
test_main_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the main page handler.
"""
import logging
import pytest
import requests
from bs4 import BeautifulSoup
from common.studio_location import StudioLocation
from datetime import date
from studios.absolute.absolute import send_get_schedule_request, get_schedule_from_response_soup, get_instructorid_map_from_response_soup, get_absolute_schedule_and_instructorid_map
from studios.absolute.data import LOCATION_MAP
from tests.studios.absolute import expected_results
from tests.studios.absolute import example_html_responses

def test_send_get_schedule_request_single_location(mocker):
  """
  Test send_get_schedule_request flow with a single location.
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
    url="https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm?action=Reserve.chooseClass",
    params={"wk": week, "site": LOCATION_MAP[locations[0]]}
  )
  assert response.status_code == 200

def test_send_get_schedule_request_multiple_locations(mocker):
  """
  Test send_get_schedule_request flow with multiple locations.
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
    url="https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm?action=Reserve.chooseClass",
    params={
      "wk": week,
      "site": LOCATION_MAP[locations[0]],
      "site2": LOCATION_MAP[locations[1]],
      "site3": LOCATION_MAP[locations[2]],
      "site4": LOCATION_MAP[locations[3]],
      "site5": LOCATION_MAP[locations[4]],
    }
  )
  assert response.status_code == 200

def test_get_schedule_from_response_soup_single_location(mocker):
  """
  Test get_schedule_from_response_soup flow with a single location.
  """
  # Setup mocks
  mock_logger = logging.getLogger("test_logger")

  mock_soup = BeautifulSoup(example_html_responses.EXAMPLE_RAFFLES_HTML_RESPONSE, "html.parser")

  # Call the function to test
  result = get_schedule_from_response_soup(mock_logger, mock_soup)

  # Assert that the response is as expected
  assert isinstance(result, dict)
  assert result.keys() == expected_results.EXPECTED_RAFFLES_SCHEDULE.keys()
  for key in result:
    assert isinstance(result, dict)
    assert (result[key] == expected_results.EXPECTED_RAFFLES_SCHEDULE[key]), (
      f"Expected result list {expected_results.EXPECTED_RAFFLES_SCHEDULE[key]} "
      f"does not match actual result list {result[key]}."
    )

def test_get_schedule_from_response_soup_multiple_locations(mocker):
  """
  Test get_schedule_from_response_soup flow with multiple locations.
  """
  # Setup mocks
  mock_logger = logging.getLogger("test_logger")

  mock_soup = BeautifulSoup(example_html_responses.EXAMPLE_MW_AND_I12_HTML_RESPONSE, "html.parser")

  # Call the function to test
  result = get_schedule_from_response_soup(mock_logger, mock_soup)

  # Assert that the response is as expected
  assert isinstance(result, dict)
  assert result.keys() == expected_results.EXPECTED_MW_AND_I12_SCHEDULE.keys()
  for key in result:
    assert isinstance(result, dict)
    assert (result[key] == expected_results.EXPECTED_MW_AND_I12_SCHEDULE[key]), (
      f"Expected result list {expected_results.EXPECTED_MW_AND_I12_SCHEDULE[key]} "
      f"does not match actual result list {result[key]}."
    )

def test_get_instructorid_map_from_response_soup_single_location(mocker):
  """
  Test get_instructorid_map_from_response_soup flow with a single location.
  """
  # Setup mocks
  mock_logger = logging.getLogger("test_logger")

  mock_soup = BeautifulSoup(example_html_responses.EXAMPLE_RAFFLES_HTML_RESPONSE, "html.parser")

  # Call the function to test
  instructorid_map = get_instructorid_map_from_response_soup(mock_logger, mock_soup)

  # Assert that the response is as expected
  assert instructorid_map == expected_results.EXPECTED_RAFFLES_INSTRUCTORID_MAP

def test_get_instructorid_map_from_response_soup_multiple_locations(mocker):
  """
  Test get_instructorid_map_from_response_soup flow with a multiple locations.
  """
  # Setup mocks
  mock_logger = logging.getLogger("test_logger")

  mock_soup = BeautifulSoup(example_html_responses.EXAMPLE_MW_AND_I12_HTML_RESPONSE, "html.parser")

  # Call the function to test
  instructorid_map = get_instructorid_map_from_response_soup(mock_logger, mock_soup)

  # Assert that the response is as expected
  assert instructorid_map == expected_results.EXPECTED_MW_AND_I12_INSTRUCTORID_MAP
