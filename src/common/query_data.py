"""
query_data.py
Author: https://github.com/lendrixxx
Description: This file defines the QueryData class used to store the details for filtering class schedules.
"""

from copy import copy
from datetime import datetime

from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


class QueryData:
    """
    Class to represent the data for filtering class schedules.

    Attributes:
      - studios (dict[StudioType, StudioData]):
        Dictionary of selected studios and the locations and instructors of the studios.
      - current_studio (StudioType): The current studio being queried.
      - weeks (int): Number of weeks to query for.
      - days (list[str]): A list of selected days for the query.
      - start_times (list[tuple[datetime.date, datetime.date]]): A list of time ranges for the query.
      - class_name_filter (str): A filter for class name for the query.

    """

    def __init__(
        self,
        studios: dict[StudioType, StudioData],
        current_studio: StudioType,
        weeks: int,
        days: list[str],
        start_times: list[tuple[datetime.date, datetime.date]],
        class_name_filter: str,
    ) -> None:
        self.studios = {} if studios is None else copy(studios)
        self.current_studio = current_studio
        self.weeks = weeks
        self.days = copy(days)
        self.start_times = copy(start_times)
        self.class_name_filter = class_name_filter

    def get_studio_locations(self, studio: StudioType) -> list[StudioLocation]:
        """
        Returns the locations to be queried for the specified studio.

        Args:
          - studio (StudioType): The studio to get the locations for.

        Returns:
          list[StudioLocation]: The list of locations to be queried for the specified studio.

        """
        if studio not in self.studios:
            return []

        return self.studios[studio].locations

    def get_selected_studios_str(self) -> str:
        """
        Returns a formatted string of the selected studios and their locations.

        Returns:
          str: A string representing the selected studios and locations.

        """
        if len(self.studios) == 0:
            return "None"

        studios_selected = ""
        for studio in self.studios:
            studios_selected += f"{studio.value} - {', '.join(self.studios[studio].locations)}\n"
        return studios_selected.rstrip()

    def get_selected_days_str(self) -> str:
        """
        Returns a formatted string of the selected days.

        Returns:
          str: A string representing the selected days.

        """
        if len(self.days) == 0:
            return "None"

        if len(self.days) == 7:
            return "All"

        return ", ".join(self.days)

    def get_selected_time_str(self) -> str:
        """
        Returns a formatted string of the selected time ranges.

        Returns:
          str: A string representing the selected time ranges.

        """
        if len(self.start_times) == 0:
            return "All"

        selected_times = ""
        for start_time_from, start_time_to in self.start_times:
            selected_times += f"{start_time_from.strftime('%H%M')} - {start_time_to.strftime('%H%M')}\n"
        return selected_times.rstrip()

    def get_selected_class_name_filter_str(self) -> str:
        """
        Returns a formatted string of the class name filter.

        Returns:
          str: The class name filter string.

        """
        if self.class_name_filter == "":
            return "None"

        return self.class_name_filter

    def get_selected_instructors_str(self) -> str:
        """
        Returns a formatted string of the selected instructors.

        Returns:
          str: A string representing the selected instructors.

        """
        if len(self.studios) == 0:
            return "None"

        instructors_selected = ""
        for studio in self.studios:
            instructor_names = ", ".join(self.studios[studio].instructors)
            instructors_selected += f"{studio.value}: {instructor_names if len(instructor_names) > 0 else 'None'}\n"
        return instructors_selected.rstrip()

    def get_query_str(
        self,
        include_studio: bool = False,
        include_instructors: bool = False,
        include_weeks: bool = False,
        include_days: bool = False,
        include_time: bool = False,
        include_class_name_filter: bool = False,
    ) -> str:
        """
        Returns a formatted string of the query based on the selected filters.

        Args:
          - include_studio (bool):
            True if the selected studios should be included in the query string, false otherwise.
          - include_instructors (bool):
            True if the selected instructors should be included in the query string, false otherwise.
          - include_weeks (bool):
            True if the number of weeks should be included in the query string, false otherwise.
          - include_days (bool):
            True if the selected days should be included in the query string, false otherwise.
          - include_time (bool):
            True if the selected time slots should be included in the query string, false otherwise.
          - include_class_name_filter (bool):
            True if the the class name filter should be included in the query string, false otherwise.

        Returns:
          str: A string representing the selected instructors.

        """
        query_str_list = []
        if include_studio:
            query_str_list.append(f"Studio(s):\n{self.get_selected_studios_str()}\n")

        if include_instructors:
            query_str_list.append(f"Instructor(s):\n{self.get_selected_instructors_str()}\n")

        if include_weeks:
            query_str_list.append(f"Week(s): {self.weeks}\n")

        if include_days:
            query_str_list.append(f"Day(s): {self.get_selected_days_str()}\n")

        if include_time:
            query_str_list.append(f"Timeslot(s):\n{self.get_selected_time_str()}\n")

        if include_class_name_filter:
            query_str_list.append(f"Class Name Filter: {self.get_selected_class_name_filter_str()}\n")

        return "\n".join(query_str_list)
