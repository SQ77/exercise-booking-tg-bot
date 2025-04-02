"""
studios_manager.py
Author: https://github.com/lendrixxx
Description: This file defines the StudioManager class which is the main handler for storing of studio data.
"""
from typing import Callable

class StudioManager:
  """
  Manages studio data.

  Attributes:
    - get_schedule_and_instructorid_map_func (Callable[..., tuple["ResultData", dict[str, int]]]):
      Callback function to get the schedule and instructor id map for the studio.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs.
    - instructor_names (list[str]): List of instructor names.
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
    self.instructor_names = []
    self.get_schedule_and_instructorid_map_func = get_schedule_and_instructorid_map_func

  def get_schedule(self, *args: any) -> "ResultData":
    """
    Retrieves the full schedule of the studio.

    Args:
      - args (any): The arguments to pass to the get_schedule_and_instructorid_map_func callback.

    Returns:
      ResultData: The full schedule of the studio.
    """
    schedule, self.instructorid_map = self.get_schedule_and_instructorid_map_func(*args)
    self.instructor_names = sorted([instructor.lower() for instructor in list(self.instructorid_map)])
    return schedule
