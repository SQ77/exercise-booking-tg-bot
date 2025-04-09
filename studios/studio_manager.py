"""
studios_manager.py
Author: https://github.com/lendrixxx
Description: This file defines the StudioManager class which is the main handler for storing of studio data.
"""
from readerwriterlock import rwlock
from typing import Callable

class StudioManager:
  """
  Manages studio data.

  Attributes:
    - get_schedule_and_instructorid_map_func (Callable[..., tuple["ResultData", dict[str, int]]]):
      Callback function to get the schedule and instructor id map for the studio.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs.
    - instructorid_map_lock (readerwriterlock.rwlock): Read-write lock for instructorid_map.
    - instructor_names (list[str]): List of instructor names.
    - instructor_names_lock (readerwriterlock.rwlock): Read-write lock for instructor_names.
  """

  def __init__(
    self,
    get_schedule_and_instructorid_map_func: Callable[..., tuple["ResultData", dict[str, int]]],
  ) -> None:
    """
    Initializes the StudioManager instance.

    Args:
      - get_schedule_and_instructorid_map_func (Callable[..., tuple["ResultData", dict[str, int]]]):
        The callback function to get the schedule and instructor id map for the studio.
    """
    self.instructorid_map = {}
    self.instructorid_map_lock = rwlock.RWLockFair()
    self.instructor_names = []
    self.instructor_names_lock = rwlock.RWLockFair()
    self.get_schedule_and_instructorid_map_func = get_schedule_and_instructorid_map_func

  def get_schedule(self, *args: any) -> "ResultData":
    """
    Retrieves the full schedule of the studio.

    Args:
      - args (any): The arguments to pass to the get_schedule_and_instructorid_map_func callback.

    Returns:
      ResultData: The full schedule of the studio.
    """
    schedule, new_instructorid_map = self.get_schedule_and_instructorid_map_func(*args)
    new_instructor_names = [instructor.lower() for instructor in list(new_instructorid_map)]
    with self.instructorid_map_lock.gen_wlock():
      self.instructorid_map.update(new_instructorid_map)

    new_instructor_names = list(set(self.instructor_names + new_instructor_names))
    new_instructor_names = sorted(new_instructor_names)
    with self.instructor_names_lock.gen_wlock():
      self.instructor_names = sorted(new_instructor_names)

    return schedule

  def get_instructorid_map(self) -> dict[str, int]:
    """
    Retrieves the dictionary of instructor names and IDs.

    Returns:
      dict[str, int]: The stored dictionary of instructor names and IDs.
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
