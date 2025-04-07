"""
barrys.py
Author: https://github.com/lendrixxx
Description:
  This file defines functions to handle the retrieving of
  class schedules and instructor IDs for Barrys studio.
"""
import re
import requests
from bs4 import BeautifulSoup
from common.capacity_info import CapacityInfo
from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.result_data import ResultData
from common.studio_type import StudioType
from common.data import RESPONSE_AVAILABILITY_MAP
from copy import copy
from datetime import datetime
from studios.barrys.data import RESPONSE_LOCATION_TO_STUDIO_LOCATION_MAP

def send_get_schedule_request(week: int) -> requests.models.Response:
  """
  Sends a GET request to retrieve the class schedule for the specified locations and week.

  Args:
    - week (int): The week number to retrieve the schedule for.

  Returns:
    - requests.models.Response: The response object containing the schedule data.
  """
  url = "https://apac.barrysbootcamp.com.au/reserve/index.cfm?action=Reserve.chooseClass"
  params = {"wk": max(0, min(week, 2)), "site": 1, "site2": 12}
  return requests.get(url=url, params=params)

def get_schedule_from_response_soup(
  logger: "logging.Logger",
  soup: BeautifulSoup,
  week: int,
) -> dict[datetime.date, list[ClassData]]:
  """
  Parses the response soup to extract the class schedule data.

  Args:
    - logger (logging.Logger): Logger for logging messages.
    - soup (BeautifulSoup): The parsed HTML response from the schedule request.
    - week (int): The week number of the retrieved schedule..

  Returns:
    - dict[datetime.date, list[ClassData]]: Dictionary of dates and details of classes.
  """
  reserve_list_div = soup.find(name="div", class_="tab-content reservelist")
  if reserve_list_div is None:
    logger.warning(f"Failed to get schedule - Reserve list not found: {soup}")
    return {}

  result_dict = {}
  for day_div in reserve_list_div.find_all(name="div", class_="tab-pane"):
    day_id = day_div.get("id")
    if day_id is None:
      logger.warning(f"Failed to get schedule of day - ID not found: {day_div}")
      continue

    current_date = datetime.strptime(day_id.strip(), "day%Y%m%d").date()
    for schedule_block in day_div.find_all(name="div", class_="scheduleBlock"):
      schedule_block_class_list = schedule_block.get("class")
      if len(schedule_block_class_list) < 2:
        availability = ClassAvailability.Null
      else:
        availability_str = schedule_block_class_list[1]
        if availability_str == "empty": # No classes available for the day
          continue
        availability = RESPONSE_AVAILABILITY_MAP[availability_str]

      schedule_class_span = schedule_block.find(name="span", class_="scheduleClass")
      if schedule_class_span is None:
        # Check if class was cancelled or is an actual error
        is_cancelled = schedule_block.find(name="span", class_="scheduleCancelled")
        if is_cancelled is None:
          logger.warning(f"Failed to get session name: {schedule_block}")
        continue

      schedule_instruc_span = schedule_block.find(name="span", class_="scheduleInstruc")
      if schedule_instruc_span is None:
        logger.warning(f"Failed to get session instructor: {schedule_block}")
        continue
      instructor_name_span = schedule_instruc_span.find(name="span")
      if instructor_name_span is None:
        logger.warning(f"Failed to get session instructor name: {schedule_instruc_span}")
        continue
      instructor = instructor_name_span.get_text().strip()
      if schedule_instruc_span.find(name="i", class_="badge substitute") is not None:
        instructor += " (S)"

      schedule_time_span = schedule_block.find(name="span", class_="scheduleTime")
      if schedule_time_span is None:
        logger.warning(f"Failed to get session time: {schedule_block}")
        continue
      schedule_time = schedule_time_span.get_text().strip()
      schedule_time = schedule_time[:schedule_time.find("M") + 1]

      schedule_site_span = schedule_block.find(name="span", class_="scheduleSite")
      if schedule_site_span is None:
        logger.warning(f"Failed to get session location: {schedule_block}")
        continue

      try:
        location = RESPONSE_LOCATION_TO_STUDIO_LOCATION_MAP[schedule_site_span.get_text().strip()]
      except:
        logger.warning(f"Failed to get session studio type for room '{room}'")
        location = StudioLocation.Unknown

      class_details = ClassData(
        studio=StudioType.Barrys,
        location=location,
        name=schedule_class_span.get_text().strip(),
        instructor=instructor,
        time=schedule_time,
        availability=availability,
        capacity_info=CapacityInfo(),
      )

      if current_date not in result_dict:
        result_dict[current_date] = [copy(class_details)]
      elif class_details in result_dict[current_date]:
        logger.warning(f"Found duplicate class {class_details.__dict__}: {day_div}")
        continue
      else:
        result_dict[current_date].append(copy(class_details))

  return result_dict

def get_instructorid_map_from_response_soup(logger: "logging.Logger", soup: BeautifulSoup) -> dict[str, int]:
  """
  Parses the response soup to extract the IDs of instructors.

  Args:
    - logger (logging.Logger): Logger for logging messages.
    - soup (BeautifulSoup): The parsed HTML response from the schedule request.

  Returns:
    - dict[str, int]: Dictionary of instructor names and IDs.
  """
  reserve_filter = soup.find(name="ul", id="reserveFilter")
  if reserve_filter is None:
    logger.warning(f"Failed to get list of instructors - Reserve filter not found: {soup}")
    return {}

  instructor_filter = reserve_filter.find(name="li", id="reserveFilter1")
  if instructor_filter is None:
    logger.warning(f"Failed to get list of instructors - Instructor filter not found: {reserve_filter}")
    return {}

  instructorid_map = {}
  for instructor in instructor_filter.find_all(name="li"):
    instructor_name = " ".join(instructor.get_text().strip().lower().split())
    instructor_name = instructor_name.replace("\n", " ")
    if instructor.a is None:
      logger.warning(f"Failed to get id of instructor {instructor_name} - A tag is null: {instructor}")
      continue

    href = instructor.a.get("href")
    if href is None:
      logger.warning(f"Failed to get id of instructor {instructor_name} - Href is null: {instructor.a}")
      continue

    match = re.search(r"instructorid=(\d+)", href)
    if match is None:
      logger.warning(f"Failed to get id of instructor {instructor_name} - Regex failed to match: {href}")
      continue

    instructorid_map[instructor_name] = match.group(1)

  return instructorid_map

def get_barrys_schedule_and_instructorid_map(logger: "logging.Logger") -> tuple[ResultData, dict[str, int]]:
  """
  Retrieves class schedules and instructor ID mappings.

  Args:
    - logger (logging.Logger): Logger for logging messages.

  Returns:
    - tuple[ResultData, dict[str, int]]: A tuple containing schedule data and instructor ID mappings.
  """
  result = ResultData()
  instructorid_map = {}

  # REST API can only select one week at a time
  # Barrys schedule only shows up to 3 weeks in advance
  for week in range(0, 3):
    get_schedule_response = send_get_schedule_request(week=week)
    soup = BeautifulSoup(markup=get_schedule_response.text, features="html.parser")

    # Get schedule
    date_class_data_list_dict = get_schedule_from_response_soup(logger=logger, soup=soup, week=week)
    result.add_classes(classes=date_class_data_list_dict)

    # Get instructor id map
    current_instructorid_map = get_instructorid_map_from_response_soup(logger=logger, soup=soup)
    instructorid_map = {**instructorid_map, **current_instructorid_map}

  return result, instructorid_map
