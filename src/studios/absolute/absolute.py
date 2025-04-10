"""
absolute.py
Author: https://github.com/lendrixxx
Description:
  This file defines functions to handle the retrieving of
  class schedules and instructor IDs for Absolute studio.
"""

import re
from copy import copy
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup

from common.capacity_info import CapacityInfo
from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.data import RESPONSE_AVAILABILITY_MAP
from common.result_data import ResultData
from common.studio_location import StudioLocation
from studios.absolute.data import LOCATION_MAP, ROOM_ID_TO_STUDIO_LOCATION_MAP, ROOM_ID_TO_STUDIO_TYPE_MAP


def send_get_schedule_request(locations: list[StudioLocation], week: int) -> requests.models.Response:
    """
    Sends a GET request to retrieve the class schedule for the specified locations and
    week.

    Args:
      - locations (list[StudioLocation]): The list of studio locations to retrieve the schedule for.
      - week (int): The week number to retrieve the schedule for.

    Returns:
      - requests.models.Response: The response object containing the schedule data.

    """
    url = "https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm?action=Reserve.chooseClass"
    params = {"wk": week}

    if "All" in locations:
        params = {**params, **{"site": 1, "site2": 2, "site3": 3, "site4": 5, "site5": 6, "site6": 8}}
    else:
        site_param_name = "site"
        for location in locations:
            params[site_param_name] = LOCATION_MAP[location]
            if site_param_name == "site":
                site_param_name = "site2"
            elif site_param_name != "site6":
                site_param_name = site_param_name[:-1] + str(int(site_param_name[-1]) + 1)
            else:
                break

    return requests.get(url=url, params=params)


def get_schedule_from_response_soup(
    logger: "logging.Logger",
    soup: BeautifulSoup,
) -> dict[datetime.date, list[ClassData]]:
    """
    Parses the response soup to extract the class schedule data.

    Args:
      - logger (logging.Logger): Logger for logging messages.
      - soup (BeautifulSoup): The parsed HTML response from the schedule request.

    Returns:
      - dict[datetime.date, list[ClassData]]: Dictionary of dates and details of classes.

    """
    schedule_table = soup.find(name="table", id="reserve", class_="scheduleTable")
    if schedule_table is None:
        logger.warning(f"Failed to get schedule - Schedule table not found: {soup}")
        return {}

    if schedule_table.thead is None:
        logger.warning(f"Failed to get schedule - Schedule table head not found: {schedule_table}")
        return {}

    if schedule_table.tbody is None:
        # No classes for the week
        return {}

    schedule_table_head_row = schedule_table.thead.find(name="tr")
    if schedule_table_head_row is None:
        logger.warning(f"Failed to get schedule - Schedule table head row not found: {schedule_table.thead}")
        return {}

    schedule_table_body_row = schedule_table.tbody.find(name="tr")
    if schedule_table_body_row is None:
        logger.warning(f"Failed to get schedule - Schedule table body row not found: {schedule_table}")
        return {}

    schedule_table_head_data_list = schedule_table_head_row.find_all(name="td")
    schedule_table_head_data_list_len = len(schedule_table_head_data_list)
    if schedule_table_head_data_list_len == 0:
        logger.warning(f"Failed to get schedule - Schedule table head data is null: {schedule_table_head_row}")
        return {}

    schedule_table_body_data_list = schedule_table_body_row.find_all(name="td")
    schedule_table_body_data_list_len = len(schedule_table_body_data_list)
    if schedule_table_body_data_list_len == 0:
        logger.warning(f"Failed to get schedule - Schedule table body data is null: {schedule_table_body_row}")
        return {}

    if schedule_table_head_data_list_len != schedule_table_body_data_list_len:
        logger.warning(
            f"Failed to get schedule - Schedule table head and body list length does not match: "
            f"Head data: {schedule_table_head_data_list}\nBody data: {schedule_table_body_data_list}"
        )
        return {}

    result_dict = {}
    current_year = datetime.now(tz=pytz.timezone("Asia/Singapore")).year
    for index, schedule_table_head_data in enumerate(schedule_table_head_data_list):
        schedule_table_body_data = schedule_table_body_data_list[index]
        date_string = schedule_table_head_data.find(name="span", class_="thead-date").get_text().strip()
        current_date = datetime.strptime(date_string, "%d.%m").date()
        current_date = current_date.replace(year=current_year)
        reserve_table_body_data_div_list = schedule_table_body_data.find_all(name="div")
        if len(reserve_table_body_data_div_list) == 0:
            # Reserve table data div might be empty because schedule is only shown up to 1.5 weeks in advance
            continue

        for reserve_table_body_data_div in reserve_table_body_data_div_list:
            reserve_table_body_data_div_class_list = reserve_table_body_data_div.get("class")
            if len(reserve_table_body_data_div_class_list) < 2:
                availability = ClassAvailability.Null  # Class is over
            else:
                availability = RESPONSE_AVAILABILITY_MAP[reserve_table_body_data_div_class_list[1]]

            schedule_class_span = reserve_table_body_data_div.find(name="span", class_="scheduleClass")
            if schedule_class_span is None:
                # Check if class was cancelled or is an actual error
                is_cancelled = reserve_table_body_data_div.find(name="span", class_="scheduleCancelled")
                if is_cancelled is None:
                    logger.warning(f"Failed to get session name: {reserve_table_body_data_div}")
                continue

            schedule_instruc_span = reserve_table_body_data_div.find(name="span", class_="scheduleInstruc")
            if schedule_instruc_span is None:
                logger.warning(f"Failed to get session instructor: {reserve_table_body_data_div}")
                continue

            schedule_time_span = reserve_table_body_data_div.find(name="span", class_="scheduleTime")
            if schedule_time_span is None:
                logger.warning(f"Failed to get session time: {reserve_table_body_data_div}")
                continue
            schedule_time = schedule_time_span.get_text().strip()
            schedule_time = schedule_time[: schedule_time.find("M") + 1]

            room = reserve_table_body_data_div.get("data-room")
            if room is None:
                logger.warning(f"Failed to get session room: {reserve_table_body_data_div}")
                continue

            try:
                studio = ROOM_ID_TO_STUDIO_TYPE_MAP[room]
            except:
                logger.warning(f"Failed to get session studio type for room '{room}'")
                studio = StudioType.AbsoluteUnknown

            try:
                location = ROOM_ID_TO_STUDIO_LOCATION_MAP[room]
            except:
                logger.warning(f"Failed to get session studio location for room '{room}'")
                location = StudioLocation.Unknown

            class_details = ClassData(
                studio=studio,
                location=location,
                name=schedule_class_span.get_text().strip(),
                instructor=schedule_instruc_span.get_text().strip(),
                time=schedule_time,
                availability=availability,
                capacity_info=CapacityInfo(),
            )

            if current_date not in result_dict:
                result_dict[current_date] = [copy(class_details)]
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
        # No classes for the week so there is no instructor filter as well
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


def get_absolute_schedule_and_instructorid_map(logger: "logging.Logger") -> tuple[ResultData, dict[str, int]]:
    """
    Retrieves class schedules and instructor ID mappings.

    Args:
      - logger (logging.Logger): Logger for logging messages.

    Returns:
      - tuple[ResultData, dict[str, int]]: A tuple containing schedule data and instructor ID mappings.

    """
    result = ResultData()
    instructorid_map = {}
    location_map_list = list(LOCATION_MAP)

    # REST API can only select one week at a time
    # Absolute schedule only shows up to 1.5 weeks in advance
    for week in range(0, 2):
        # REST API can only select maximum of 5 locations at a time, but there are 6 locations
        # Send first request for first location
        locations = location_map_list[0:1]
        get_schedule_response = send_get_schedule_request(locations=locations, week=week)
        soup = BeautifulSoup(markup=get_schedule_response.text, features="html.parser")

        # Get schedule
        date_class_data_list_dict = get_schedule_from_response_soup(
            logger=logger,
            soup=soup,
        )
        result.add_classes(classes=date_class_data_list_dict)

        # Get instructor id map
        current_instructorid_map = get_instructorid_map_from_response_soup(logger=logger, soup=soup)
        instructorid_map = {**instructorid_map, **current_instructorid_map}

        # Send second request for last 5 locations
        locations = location_map_list[1:]
        get_schedule_response = send_get_schedule_request(locations=locations, week=week)

        # Get schedule
        soup = BeautifulSoup(markup=get_schedule_response.text, features="html.parser")
        date_class_data_list_dict = get_schedule_from_response_soup(
            logger=logger,
            soup=soup,
        )
        result.add_classes(classes=date_class_data_list_dict)

        # Get instructor id map
        current_instructorid_map = get_instructorid_map_from_response_soup(logger=logger, soup=soup)
        instructorid_map = {**instructorid_map, **current_instructorid_map}

    return result, instructorid_map
