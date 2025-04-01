"""
studios_manager.py
Author: https://github.com/lendrixxx
Description:
  This file defines the StudiosManager class which is the main handler for retrieving and storing of studio data.
"""
import schedule
import threading
import time
from common.result_data import ResultData
from copy import deepcopy
from readerwriterlock import rwlock
from studios.absolute.absolute import get_absolute_schedule_and_instructorid_map
from studios.ally.ally import get_ally_schedule_and_instructorid_map
from studios.anarchy.anarchy import get_anarchy_schedule_and_instructorid_map
from studios.barrys.barrys import get_barrys_schedule_and_instructorid_map
from studios.rev.rev import get_rev_schedule_and_instructorid_map
from studios.studio_manager import StudioManager

class StudiosManager:
  """
  Manages studios data.

  Attributes:
    - logger (logging.Logger): Logger for logging messages.
    - cached_result_data_lock (readerwriterlock.rwlock): Read-write lock for cached_result_data.
    - cached_result_data (ResultData): Cached result data containing schedules of all the studios.
    - studios (dict[StudioType, StudioManager]): Dictionary of studio types and studio managers.
  """

  def __init__(self, logger: "logging.Logger") -> None:
    """
    Initializes the StudiosManager instance.

    Args:
      - logger (logging.Logger): The logger for logging messages.
    """
    self.logger = logger
    self.cached_result_data_lock = rwlock.RWLockFair()
    self.cached_result_data = ResultData()
    self.studios = {
      "Absolute": StudioManager(self.logger, get_absolute_schedule_and_instructorid_map),
      "Ally": StudioManager(self.logger, get_ally_schedule_and_instructorid_map),
      "Anarchy": StudioManager(self.logger, get_anarchy_schedule_and_instructorid_map),
      "Barrys": StudioManager(self.logger, get_barrys_schedule_and_instructorid_map),
      "Rev": StudioManager(self.logger, get_rev_schedule_and_instructorid_map)
    }

  def update_cached_result_data(self) -> None:
    """
    Updates the cached schedule data from all studios.
    """
    def _get_absolute_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      absolute_schedule = self.studios["Absolute"].get_schedule()
      with mutex:
        updated_cached_result_data += absolute_schedule

    def _get_ally_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      ally_schedule = self.studios["Ally"].get_schedule()
      with mutex:
        updated_cached_result_data += ally_schedule

    def _get_anarchy_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      anarchy_schedule = self.studios["Anarchy"].get_schedule()
      with mutex:
        updated_cached_result_data += anarchy_schedule

    def _get_barrys_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      barrys_schedule = self.studios["Barrys"].get_schedule()
      with mutex:
        updated_cached_result_data += barrys_schedule

    def _get_rev_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      rev_schedule = self.studios["Rev"].get_schedule()
      with mutex:
        updated_cached_result_data += rev_schedule

    self.logger.info("Updating cached result data...")
    updated_cached_result_data = ResultData()
    mutex = threading.Lock()

    threads = []
    for func, name in [
      (_get_absolute_schedule, "absolute_thread"),
      (_get_ally_schedule, "ally_thread"),
      (_get_anarchy_schedule, "anarchy_thread"),
      (_get_barrys_schedule, "barrys_thread"),
      (_get_rev_schedule, "rev_thread")
    ]:
      thread = threading.Thread(target=func, name=name, args=[self, mutex, updated_cached_result_data], daemon=True)
      threads.append(thread)
      thread.start()

    for thread in threads:
      thread.join()

    with self.cached_result_data_lock.gen_wlock():
      self.cached_result_data = updated_cached_result_data
    self.logger.info("Successfully updated cached result data!")

  def schedule_update_cached_result_data(self) -> None:
    """
    Periodically updates cached schedule data.
    Scheduled runs is triggered in main thread.
    """
    schedule.every(10).minutes.do(job_func=self.update_cached_result_data)

  def start(self) -> None:
    """
    Starts the scheduling manager by updating the cached result data.
    """
    self.update_cached_result_data()

  def get_cached_result_data(self) -> ResultData:
    """
    Retrieves the cached result data.

    Returns:
      ResultData: The stored cached result data.
    """
    with self.cached_result_data_lock.gen_rlock():
      return deepcopy(self.cached_result_data)

