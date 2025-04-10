"""
result_data.py
Author: https://github.com/lendrixxx
Description:
  This file defines the ResultData class used to store class schedules and
  provide functionality for filtering classes based on various query parameters.
"""

import calendar
from copy import copy
from datetime import datetime, timedelta

import pytz

from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.query_data import QueryData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


class ResultData:
    """
    Class to represent the data for class schedules of various studios.

    Attributes:
      - classes (dict[datetime.date, list[ClassData]]): Dictionary of dates and details of classes.

    """

    def __init__(self, classes: dict[datetime.date, list[ClassData]] = None) -> None:
        """
        Initializes the ResultData instance.

        Args:
          - classes (dict[datetime.date, list[ClassData]]): The dictionary of dates and details of classes.

        """
        self.classes = {} if classes is None else classes

    def add_class(self, date: datetime.date, data: ClassData) -> None:
        """
        Adds a class to the given date.

        Args:
          - date (datetime.date): The date of the class.
          - data (ClassData): The class data to be added.

        """
        if date not in self.classes:
            self.classes[date] = []

        self.classes[date].append(data)

    def add_classes(self, classes: dict[datetime.date, list[ClassData]]) -> None:
        """
        Adds classes to the given date.

        Args:
          - classes (dict[datetime.date, list[ClassData]]): The dictionary of dates and details of classes to add.

        """
        if classes is None:
            return

        if self.classes is None:
            self.classes = {}

        for date in classes:
            if date in self.classes:
                self.classes[date] += classes[date]
            else:
                self.classes[date] = copy(classes[date])

    def get_data(self, query: QueryData) -> "ResultData":
        """
        Filters and retrieves class data based on the provided query parameters.

        Args:
          - query (QueryData): The query parameters for filtering class data.

        Returns:
          ResultData: A new ResultData instance containing the filtered class data.

        """
        if self.classes is None:
            return ResultData()

        classes = {}
        current_sg_time = datetime.now(tz=pytz.timezone("Asia/Singapore"))
        for week in range(0, query.weeks):
            date_to_check = datetime.now(tz=pytz.timezone("Asia/Singapore")).date() + timedelta(weeks=week)
            for day in range(7):
                if "All" not in query.days and calendar.day_name[date_to_check.weekday()] not in query.days:
                    date_to_check = date_to_check + timedelta(days=1)
                    continue

                if date_to_check in self.classes:
                    for class_details in self.classes[date_to_check]:
                        if class_details.studio not in query.studios:
                            continue

                        if (
                            query.class_name_filter != ""
                            and query.class_name_filter.lower() not in class_details.name.lower()
                        ):
                            continue

                        query_locations = query.get_studio_locations(class_details.studio)
                        if StudioLocation.All not in query_locations and class_details.location not in query_locations:
                            continue

                        is_by_instructor = (
                            "All" in query.studios[class_details.studio].instructors
                            or class_details.studio == StudioType.AllyRecovery
                            or any(
                                instructor.lower() == class_details.instructor.lower()
                                for instructor in query.studios[class_details.studio].instructors
                            )
                            or any(
                                instructor.lower() in class_details.instructor.lower().split(" ")
                                for instructor in query.studios[class_details.studio].instructors
                            )
                            or any(
                                instructor.lower() == class_details.instructor.lower().split(".")[0]
                                for instructor in query.studios[class_details.studio].instructors
                            )
                        )
                        if not is_by_instructor:
                            continue

                        class_time = datetime.strptime(class_details.time, "%I:%M %p")
                        if week == 0 and day == 0:  # Skip classes that have already ended
                            if (
                                current_sg_time.hour > class_time.hour
                                or current_sg_time.hour == class_time.hour
                                and current_sg_time.minute > class_time.minute
                            ):
                                continue

                        if len(query.start_times) > 0:
                            within_start_times = False
                            for start_time_from, start_time_to in query.start_times:
                                class_time_within_query_time_from = (
                                    class_time.hour > start_time_from.hour
                                    or class_time.hour == start_time_from.hour
                                    and class_time.minute >= start_time_from.minute
                                )
                                class_time_within_query_time_to = (
                                    class_time.hour < start_time_to.hour
                                    or class_time.hour == start_time_to.hour
                                    and class_time.minute <= start_time_to.minute
                                )
                                if class_time_within_query_time_from and class_time_within_query_time_to:
                                    within_start_times = True
                                    break

                            if not within_start_times:
                                continue

                        classes.setdefault(date_to_check, []).append(class_details)
                date_to_check = date_to_check + timedelta(days=1)

        result = ResultData(classes)
        return result

    def get_result_str(self) -> str:
        """
        Returns a formatted string of the classes.

        Returns:
          str: A string representing the classes.

        """
        if len(self.classes) == 0:
            return "No classes found"

        result_str = ""
        for date in sorted(self.classes):
            date_str = f"*{calendar.day_name[date.weekday()]}, {date.strftime('%d %B')}*"
            result_str += f"{date_str}\n"

            for class_details in sorted(self.classes[date]):
                availability_str = ""
                if class_details.availability == ClassAvailability.Waitlist:
                    availability_str = "[W] "
                elif class_details.availability == ClassAvailability.Full:
                    availability_str = "[F] "
                elif class_details.availability == ClassAvailability.Cancelled:
                    availability_str = "[Cancelled] "

                if class_details.location == StudioLocation.Null:
                    result_str += (
                        f"*{availability_str + class_details.time}* - "
                        f"{class_details.name} ({class_details.instructor})"
                    )
                else:
                    result_str += (
                        f"*{availability_str + class_details.time}* - {class_details.name} "
                        f"@ {class_details.location.value} ({class_details.instructor})"
                    )

                if class_details.capacity_info.has_info:
                    if class_details.availability == ClassAvailability.Waitlist:
                        result_str += f" - {class_details.capacity_info.waitlist_reserved} Rider(s) on Waitlist"
                    else:
                        result_str += f" - {class_details.capacity_info.remaining} Spot(s) Remaining"

                result_str += "\n"
            result_str += "\n"

        return result_str

    def __add__(self, other: "ResultData") -> "ResultData":
        """
        Merges two ResultData instances.

        Args:
          - other (ResultData): The other ResultData object to add.

        Returns:
          ResultData: The combined ResultData instance.

        """
        result = self
        result.add_classes(classes=other.classes)
        return result
