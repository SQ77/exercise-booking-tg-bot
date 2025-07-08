"""
studios_manager.py
Author: https://github.com/lendrixxx
Description:
  This file defines the StudiosManager class which is the main handler for retrieving and storing of studio data.
"""

import logging
import threading
from copy import deepcopy

import schedule
from readerwriterlock.rwlock import RWLockFair

from common.result_data import ResultData
from common.studio_type import StudioType
from studios.anarchy.anarchy import get_anarchy_schedule_and_instructorid_map
from studios.barrys.barrys import get_barrys_schedule_and_instructorid_map
from studios.hapana.data.rev import LOCATION_TO_SITE_ID_MAP as REV_LOCATION_TO_SITE_ID_MAP
from studios.hapana.data.rev import ROOM_NAME_TO_STUDIO_LOCATION_MAP as REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP
from studios.hapana.data.rev import ROOM_NAME_TO_STUDIO_TYPE_MAP as REV_ROOM_NAME_TO_STUDIO_TYPE_MAP
from studios.hapana.hapana import get_hapana_schedule_and_instructorid_map, get_hapana_security_token
from studios.studio_manager import StudioManager
from studios.zingfit.data.absolute import LOCATION_TO_SITE_ID_MAP as ABSOLUTE_LOCATION_TO_SITE_ID_MAP
from studios.zingfit.data.absolute import MAX_SCHEDULE_WEEKS as ABSOLUTE_MAX_SCHEDULE_WEEKS
from studios.zingfit.data.absolute import ROOM_ID_TO_STUDIO_LOCATION_MAP as ABSOLUTE_ROOM_ID_TO_STUDIO_LOCATION_MAP
from studios.zingfit.data.absolute import ROOM_ID_TO_STUDIO_TYPE_MAP as ABSOLUTE_ROOM_ID_TO_STUDIO_TYPE_MAP
from studios.zingfit.data.absolute import TABLE_HEADING_DATE_FORMAT as ABSOLUTE_TABLE_HEADING_DATE_FORMAT
from studios.zingfit.data.absolute import URL_SUBDOMAIN as ABSOLUTE_URL_SUBDOMAIN
from studios.zingfit.data.ally import LOCATION_TO_SITE_ID_MAP as ALLY_LOCATION_TO_SITE_ID_MAP
from studios.zingfit.data.ally import MAX_SCHEDULE_WEEKS as ALLY_MAX_SCHEDULE_WEEKS
from studios.zingfit.data.ally import ROOM_ID_TO_STUDIO_LOCATION_MAP as ALLY_ROOM_ID_TO_STUDIO_LOCATION_MAP
from studios.zingfit.data.ally import ROOM_ID_TO_STUDIO_TYPE_MAP as ALLY_ROOM_ID_TO_STUDIO_TYPE_MAP
from studios.zingfit.data.ally import TABLE_HEADING_DATE_FORMAT as ALLY_TABLE_HEADING_DATE_FORMAT
from studios.zingfit.data.ally import URL_SUBDOMAIN as ALLY_URL_SUBDOMAIN
from studios.zingfit.data.ally import clean_class_name as ally_clean_class_name_func
from studios.zingfit.zingfit import get_zingfit_schedule_and_instructorid_map


class StudiosManager:
    """
    Manages studios data.

    Attributes:
      - logger (logging.Logger): Logger for logging messages.
      - cached_result_data_lock (RWLockFair): Read-write lock for cached_result_data.
      - cached_result_data (ResultData): Cached result data containing schedules of all the studios.
      - studios (dict[StudioType, StudioManager]): Dictionary of studio types and studio managers.

    """

    logger: logging.Logger
    cached_result_data_lock: RWLockFair
    cached_result_data: ResultData
    studios: dict[StudioType, StudioManager]

    def __init__(self, logger: logging.Logger) -> None:
        """
        Initializes the StudiosManager instance.

        Args:
          - logger (logging.Logger): The logger for logging messages.

        """
        self.logger = logger
        self.cached_result_data_lock = RWLockFair()
        self.cached_result_data = ResultData()
        self.studios = {
            "Absolute": StudioManager(
                get_schedule_and_instructorid_map_func=get_zingfit_schedule_and_instructorid_map,
                logger=logger,
                studio_name="Absolute",
                studio_url_subdomain=ABSOLUTE_URL_SUBDOMAIN,
                table_heading_date_format=ABSOLUTE_TABLE_HEADING_DATE_FORMAT,
                max_weeks=ABSOLUTE_MAX_SCHEDULE_WEEKS,
                location_to_site_id_map=ABSOLUTE_LOCATION_TO_SITE_ID_MAP,
                room_id_to_studio_type_map=ABSOLUTE_ROOM_ID_TO_STUDIO_TYPE_MAP,
                room_id_to_studio_location_map=ABSOLUTE_ROOM_ID_TO_STUDIO_LOCATION_MAP,
                clean_class_name_func=None,
            ),
            "Ally": StudioManager(
                get_schedule_and_instructorid_map_func=get_zingfit_schedule_and_instructorid_map,
                logger=logger,
                studio_name="Ally",
                studio_url_subdomain=ALLY_URL_SUBDOMAIN,
                table_heading_date_format=ALLY_TABLE_HEADING_DATE_FORMAT,
                max_weeks=ALLY_MAX_SCHEDULE_WEEKS,
                location_to_site_id_map=ALLY_LOCATION_TO_SITE_ID_MAP,
                room_id_to_studio_type_map=ALLY_ROOM_ID_TO_STUDIO_TYPE_MAP,
                room_id_to_studio_location_map=ALLY_ROOM_ID_TO_STUDIO_LOCATION_MAP,
                clean_class_name_func=ally_clean_class_name_func,
            ),
            "Anarchy": StudioManager(
                get_schedule_and_instructorid_map_func=get_anarchy_schedule_and_instructorid_map,
                logger=logger,
            ),
            "Barrys": StudioManager(
                get_schedule_and_instructorid_map_func=get_barrys_schedule_and_instructorid_map,
                logger=logger,
            ),
            "Rev": StudioManager(
                get_schedule_and_instructorid_map_func=get_hapana_schedule_and_instructorid_map,
                logger=logger,
                studio_name="Rev",
                security_token=get_hapana_security_token(
                    logger=logger,
                    studio_name="Rev",
                    site_id=next(iter(REV_LOCATION_TO_SITE_ID_MAP.values())),  # Get the first value from the map
                ),
                location_to_site_id_map=REV_LOCATION_TO_SITE_ID_MAP,
                room_id_to_studio_type_map=REV_ROOM_NAME_TO_STUDIO_TYPE_MAP,
                room_name_to_studio_location_map=REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP,
            ),
        }

    def update_cached_result_data(self) -> None:
        """
        Updates the cached schedule data from all studios.
        """

        def _get_absolute_schedule(
            self: StudiosManager, mutex: threading.Lock, updated_cached_result_data: ResultData
        ) -> None:
            absolute_schedule = self.studios["Absolute"].get_schedule()
            with mutex:
                updated_cached_result_data += absolute_schedule

        def _get_ally_schedule(
            self: StudiosManager, mutex: threading.Lock, updated_cached_result_data: ResultData
        ) -> None:
            ally_schedule = self.studios["Ally"].get_schedule()
            with mutex:
                updated_cached_result_data += ally_schedule

        def _get_anarchy_schedule(
            self: StudiosManager, mutex: threading.Lock, updated_cached_result_data: ResultData
        ) -> None:
            anarchy_schedule = self.studios["Anarchy"].get_schedule()
            with mutex:
                updated_cached_result_data += anarchy_schedule

        def _get_barrys_schedule(
            self: StudiosManager, mutex: threading.Lock, updated_cached_result_data: ResultData
        ) -> None:
            barrys_schedule = self.studios["Barrys"].get_schedule()
            with mutex:
                updated_cached_result_data += barrys_schedule

        def _get_rev_schedule(
            self: StudiosManager, mutex: threading.Lock, updated_cached_result_data: ResultData
        ) -> None:
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
            (_get_rev_schedule, "rev_thread"),
        ]:
            thread = threading.Thread(
                target=func, name=name, args=[self, mutex, updated_cached_result_data], daemon=True
            )
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
