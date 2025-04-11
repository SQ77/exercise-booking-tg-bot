"""
rev.py
Author: https://github.com/lendrixxx
Description:
  This file defines functions to handle the retrieving of
  class schedules and instructor IDs for Rev studio.
"""

import json
import logging
from copy import copy
from datetime import date, datetime, timedelta

import pytz
import requests

from common.capacity_info import CapacityInfo
from common.class_data import ClassData
from common.data import RESPONSE_AVAILABILITY_MAP
from common.result_data import ResultData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from studios.rev.data import ROOM_NAME_TO_STUDIO_LOCATION_MAP, SITE_ID_MAP


def send_get_schedule_request(
    location: StudioLocation,
    start_date: date,
    end_date: datetime,
    security_token: str,
) -> requests.models.Response:
    """
    Sends a GET request to retrieve the class schedule for the specified locations and
    week.

    Args:
      - location (StudioLocation): The studio location to retrieve the schedule for.
      - start_date (date): The start date to retrieve the schedule for.
      - end_date (date): The end date to retrieve the schedule for.
      - security_token (str): Security token used for sending requests.

    Returns:
      - requests.models.Response: The response object containing the schedule data.

    """
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    url = "https://widgetapi.hapana.com/v2/wAPI/site/sessions?sessionCategory=classes"
    params = {"siteID": SITE_ID_MAP[location], "startDate": start_date_str, "endDate": end_date_str}
    headers = {
        "Content-Type": "application/json",
        "Securitytoken": security_token,
    }
    return requests.get(url=url, params=params, headers=headers)


def parse_get_schedule_response(
    logger: logging.Logger,
    response: requests.models.Response,
) -> dict[date, list[ClassData]]:
    """
    Parses the get schedule response to extract the class schedule data.

    Args:
      - logger (logging.Logger): Logger for logging messages.
      - response: The get schedule response from the schedule request.

    Returns:
      - dict[date, list[ClassData]]: Dictionary of dates and details of classes.

    """
    if response.status_code != 200:
        logger.warning(f"Failed to get schedule - API callback error {response.status_code}")
        return {}

    result_dict = {}
    try:
        response_json = json.loads(s=response.text)
        if "success" not in response_json:
            logger.warning(f"Failed to get schedule - API callback failed: {response_json}")
            return {}
    except Exception as e:
        logger.warning(f"Failed to get schedule - {e}: {response.text}")
        return {}

    for data in response_json["data"]:
        try:
            if data["sessionStatus"] == "complete":
                continue

            class_date = datetime.strptime(data["sessionDate"], "%Y-%m-%d").date()
            instructors = []
            for instructorData in data["instructorData"]:
                instructors.append(instructorData["instructorName"])
            instructor_str = " / ".join(instructors)

            class_name = data["sessionName"]
            class_name_location_split_pos = class_name.find(" @ ")
            class_name = class_name[:class_name_location_split_pos]
            class_time = datetime.strptime(data["startTime"], "%H:%M:%S")

            if data["roomName"] in ROOM_NAME_TO_STUDIO_LOCATION_MAP:
                location = ROOM_NAME_TO_STUDIO_LOCATION_MAP[data["roomName"]]
            else:
                location = StudioLocation.Null
                class_name += " @ " + data["roomName"]

            class_details = ClassData(
                studio=StudioType.Rev,
                location=location,
                name=class_name,
                instructor=instructor_str,
                time=class_time.strftime("%I:%M %p").lstrip("0"),
                availability=RESPONSE_AVAILABILITY_MAP[data["sessionStatus"]],
                capacity_info=CapacityInfo(
                    has_info=True,
                    capacity=data["capacity"],
                    remaining=data["remaining"],
                    waitlist_capacity=data["waitlistCapacity"],
                    waitlist_reserved=data["waitlistReserved"],
                ),
            )

            if class_date not in result_dict:
                result_dict[class_date] = [copy(class_details)]
            else:
                result_dict[class_date].append(copy(class_details))

        except Exception as e:
            logger.warning(f"Failed to get details of class - {e}. Data: {data}")

    return result_dict


def get_rev_schedule(logger: logging.Logger, security_token: str) -> ResultData:
    """
    Retrieves all the available class schedules.

    Args:
      - logger (logging.Logger): Logger for logging messages.
      - security_token (str): Security token used for sending requests.

    Returns:
      - ResultData: The schedule data.

    """
    result = ResultData()
    start_date = datetime.now(tz=pytz.timezone("Asia/Singapore"))
    end_date = start_date + timedelta(weeks=4)  # Rev schedule only shows up to 4 weeks in advance

    # REST API can only select one location at a time
    for location in ["Bugis", "Orchard", "TJPG"]:
        get_schedule_response = send_get_schedule_request(
            location=location,
            start_date=start_date,
            end_date=end_date,
            security_token=security_token,
        )
        date_class_data_list_dict = parse_get_schedule_response(logger=logger, response=get_schedule_response)
        result.add_classes(classes=date_class_data_list_dict)

    return result


def get_instructorid_map(logger: logging.Logger, security_token: str) -> dict[str, str]:
    """
    Retrieves the IDs of instructors.

    Args:
      - logger (logging.Logger): Logger for logging messages.
      - security_token (str): Security token used for sending requests.

    Returns:
      - dict[str, str]: Dictionary of instructor names and IDs.

    """
    url = "https://widgetapi.hapana.com/v2/wAPI/site/instructor"
    headers = {
        "Content-Type": "application/json",
        "Securitytoken": security_token,
    }
    # REST API can only select one location at a time
    instructorid_map: dict[str, str] = {}
    for location in ["Bugis", "Orchard", "TJPG"]:
        params = {"siteID": SITE_ID_MAP[location]}
        response = requests.get(url=url, params=params, headers=headers)
        if response.status_code != 200:
            logger.warning(
                f"Failed to get list of instructors for {location} - API callback error {response.status_code}"
            )
            continue

        try:
            response_json = json.loads(s=response.text)
            if not response_json["success"]:
                logger.warning(
                    f"Failed to get list of instructors for {location} - API callback failed: {response_json}"
                )
                continue

            for data in response_json["data"]:
                instructorid_map[data["instructorName"].lower()] = data["instructorID"]

        except Exception as e:
            logger.warning(f"Failed to get list of instructors for {location} - {e}")
            continue

    return instructorid_map


def get_rev_schedule_and_instructorid_map(
    logger: logging.Logger,
    security_token: str,
) -> tuple[ResultData, dict[str, str]]:
    """
    Retrieves class schedules and instructor ID mappings.

    Args:
      - logger (logging.Logger): Logger for logging messages.
      - security_token (str): Security token used for sending requests.

    Returns:
      - tuple[ResultData, dict[str, str]]: A tuple containing schedule data and instructor ID mappings.

    """
    return (
        get_rev_schedule(logger=logger, security_token=security_token),
        get_instructorid_map(logger=logger, security_token=security_token),
    )
