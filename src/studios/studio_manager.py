"""
studios_manager.py
Author: https://github.com/lendrixxx
Description: This file defines the StudioManager class which is the main handler for storing of studio data.
"""

from functools import partial
from typing import Any, Callable

from readerwriterlock.rwlock import RWLockFair

from common.result_data import ResultData


class StudioManager:
    """
    Manages studio data.

    Attributes:
      - get_schedule_and_instructorid_map_func (Callable[..., tuple[ResultData, dict[str, str]]]):
        Callback function to get the schedule and instructor id map for the studio.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs.
      - instructorid_map_lock (RWLockFair): Read-write lock for instructorid_map.
      - instructor_names (list[str]): List of instructor names.
      - instructor_names_lock (RWLockFair): Read-write lock for instructor_names.

    """

    get_schedule_and_instructorid_map_func: Callable[..., tuple[ResultData, dict[str, str]]]
    instructorid_map: dict[str, str]
    instructorid_map_lock: RWLockFair
    instructor_names: list[str]
    instructor_names_lock: RWLockFair

    def __init__(
        self,
        get_schedule_and_instructorid_map_func: Callable[..., tuple[ResultData, dict[str, str]]],
        **kwargs: Any,
    ) -> None:
        """
        Initializes the StudioManager instance.

        Args:
          - get_schedule_and_instructorid_map_func (Callable[..., tuple[ResultData, dict[str, str]]]):
            The callback function to get the schedule and instructor id map for the studio.
          - kwargs (Any): The keyword arguments to pass to the get_schedule_and_instructorid_map_func callback.

        """
        self.instructorid_map: dict[str, str] = {}
        self.instructorid_map_lock = RWLockFair()
        self.instructor_names: list[str] = []
        self.instructor_names_lock = RWLockFair()
        self.get_schedule_and_instructorid_map_func = partial(get_schedule_and_instructorid_map_func, **kwargs)

    def get_schedule(self) -> ResultData:
        """
        Retrieves the full schedule of the studio.

        Returns:
          ResultData: The full schedule of the studio.

        """
        schedule, new_instructorid_map = self.get_schedule_and_instructorid_map_func()
        new_instructor_names = [instructor.lower() for instructor in list(new_instructorid_map)]
        with self.instructorid_map_lock.gen_wlock():
            self.instructorid_map.update(new_instructorid_map)

        new_instructor_names = list(set(self.instructor_names + new_instructor_names))
        new_instructor_names = sorted(new_instructor_names)
        with self.instructor_names_lock.gen_wlock():
            self.instructor_names = sorted(new_instructor_names)

        return schedule

    def get_instructorid_map(self) -> dict[str, str]:
        """
        Retrieves the dictionary of instructor names and IDs.

        Returns:
          dict[str, str]: The stored dictionary of instructor names and IDs.

        """
        with self.instructorid_map_lock.gen_rlock():
            return self.instructorid_map.copy()

    def get_instructor_names(self) -> list[str]:
        """
        Retrieves the list of instructor names.

        Returns:
          list[str]: The stored list of instructor names.

        """
        with self.instructor_names_lock.gen_rlock():
            return self.instructor_names.copy()
