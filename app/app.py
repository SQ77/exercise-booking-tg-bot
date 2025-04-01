"""
app.py
Author: https://github.com/lendrixxx
Description:
  This file defines the App class which is the main application for the Studios Schedule Checker Telegram Bot.
  This application allows users to check class availabilities of various studios through a Telegram bot.
"""
import logging
import os
import telebot
import threading
import time
import schedule
import signal
from chat.chat_manager import ChatManager
from chat.keyboard_manager import KeyboardManager
from common.result_data import ResultData
from history.history_manager import HistoryManager
from menu.menu_manager import MenuManager
from server.server import Server
from studios.absolute.absolute import get_absolute_schedule_and_instructorid_map
from studios.ally.ally import get_ally_schedule_and_instructorid_map
from studios.anarchy.anarchy import get_anarchy_schedule_and_instructorid_map
from studios.barrys.barrys import get_barrys_schedule_and_instructorid_map
from studios.rev.rev import get_rev_schedule_and_instructorid_map
from studios.studios_manager import StudioManager, StudiosManager

class App:
  """
  Main application class for the Studios Schedule Checker Telegram Bot.

  This class initializes and manages the bot, schedules updates,
  handles server interactions, and runs the application.
  """

  def __init__(self) -> None:
    """
    Initializes the App instance.

    Sets up logging, initializes the Telegram bot with commands,
    and initializes various managers for handling schedules, history,
    server interactions, and menus.
    """
    self.logger = logging.getLogger(__name__)
    logging.basicConfig(
      format="%(asctime)s %(filename)s:%(lineno)d [%(levelname)-1s] %(message)s",
      level=logging.INFO,
      datefmt="%d-%m-%Y %H:%M:%S")

    bot_token = os.environ.get("BOT_TOKEN")
    self.bot = telebot.TeleBot(token=bot_token)
    start_command = telebot.types.BotCommand(command="start", description="Check schedules")
    nerd_command = telebot.types.BotCommand(command="nerd", description="Nerd mode")
    instructors_command = telebot.types.BotCommand(command="instructors", description="Show list of instructors")
    self.bot.set_my_commands(commands=[start_command, nerd_command, instructors_command])

    self.keyboard_manager = KeyboardManager()
    self.chat_manager = ChatManager(bot=self.bot)
    self.studios_manager = StudiosManager(
      {
        "Absolute": StudioManager(self.logger, get_absolute_schedule_and_instructorid_map),
        "Ally": StudioManager(self.logger, get_ally_schedule_and_instructorid_map),
        "Anarchy": StudioManager(self.logger, get_anarchy_schedule_and_instructorid_map),
        "Barrys": StudioManager(self.logger, get_barrys_schedule_and_instructorid_map),
        "Rev": StudioManager(self.logger, get_rev_schedule_and_instructorid_map)
      },
    )

    self.history_manager = HistoryManager(logger=self.logger)
    self.server = Server(logger=self.logger)
    self.menu_manager = MenuManager(
      logger=self.logger,
      bot=self.bot,
      chat_manager=self.chat_manager,
      keyboard_manager=self.keyboard_manager,
      studios_manager=self.studios_manager,
      history_manager=self.history_manager,
    )
    self.bot_polling_thread = None
    self.server_thread = None
    self.update_schedule_thread = None

  def update_cached_result_data(self) -> None:
    """
    Updates the cached schedule data from all studios.
    """
    def _get_absolute_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      absolute_schedule = self.studios_manager["Absolute"].get_schedule()
      with mutex:
        updated_cached_result_data += absolute_schedule

    def _get_ally_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      ally_schedule = self.studios_manager["Ally"].get_schedule()
      with mutex:
        updated_cached_result_data += ally_schedule

    def _get_anarchy_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      anarchy_schedule = self.studios_manager["Anarchy"].get_schedule()
      with mutex:
        updated_cached_result_data += anarchy_schedule

    def _get_barrys_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      barrys_schedule = self.studios_manager["Barrys"].get_schedule()
      with mutex:
        updated_cached_result_data += barrys_schedule

    def _get_rev_schedule(self, mutex: threading.Lock, updated_cached_result_data: ResultData) -> None:
      rev_schedule = self.studios_manager["Rev"].get_schedule()
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

    self.menu_manager.cached_result_data = updated_cached_result_data
    self.logger.info("Successfully updated cached result data!")

  def schedule_update_cached_result_data(self, stop_event: threading.Event) -> None:
    """
    Periodically updates cached schedule data.

    Args:
      - stop_event (threading.Event): Event that signals if execution should be stopped.
    """
    schedule.every(10).minutes.do(job_func=self.update_cached_result_data)
    schedule.every(10).minutes.do(job_func=self.server.ping_self)

    while not stop_event.is_set():
      schedule.run_pending()
      time.sleep(1)

  def start_bot_polling(self) -> None:
    """
    Starts the TeleBot's polling mechanism to listen for messages and callback queries.
    """
    self.bot.infinity_polling(allowed_updates=['message', 'callback_query'])

  def shutdown(self, _: int, __: "types.FrameType") -> None:
    """
    Gracefully shuts down the bot and background threads.

    Args:
      - _ (int): Signal number received, but not used in this function.
      - __ (types.FrameType): Current stack frame at the time of signal reception, but not used in this function.
    """
    self.logger.info("Received termination signal. Stopping bot and background threads...")
    self.bot.stop_polling()

    # Signal threads to stop
    self.stop_event.set()

    # Wait for non-daemon threads to stop
    if self.bot_polling_thread.is_alive():
      self.bot_polling_thread.join()

    self.logger.info("Successfully exited")
    exit(0)

  def run(self) -> None:
    """
    Starts the application and runs all necessary processes.
    """
    # Load existing history
    self.history_manager.start()

    # Create threads
    self.stop_event = threading.Event()

    # Setup threads
    self.server_thread = threading.Thread(target=self.server.start_server, daemon=True)
    self.update_schedule_thread = threading.Thread(
      target=self.schedule_update_cached_result_data,
      args=[self.stop_event],
      daemon=True,
    )
    self.bot_polling_thread = threading.Thread(target=self.start_bot_polling)

    # Register signal handlers
    signal.signal(signalnum=signal.SIGTERM, handler=self.shutdown)
    signal.signal(signalnum=signal.SIGINT, handler=self.shutdown)

    # Get current schedule and store in cache
    self.update_cached_result_data()

    # Start threads
    self.logger.info("Starting bot...")
    self.server_thread.start()
    self.update_schedule_thread.start()
    self.bot_polling_thread.start()
    self.logger.info("Bot started!")

    # Keep the main thread alive
    while not self.stop_event.is_set():
      time.sleep(1)
