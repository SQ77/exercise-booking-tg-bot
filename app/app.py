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
from studios.studios_manager import StudioManager, StudiosManager

class App:
  """
  Main application class for the Studios Schedule Checker Telegram Bot.
  This class initializes and manages the bot, schedules updates,
  handles server interactions, and runs the application.

  Attributes:
    - logger (logging.Logger): Logger for logging messages.
    - bot (telebot.TeleBot): The Telegram bot instance.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
    - studios_manager (StudiosManager): The manager handling studios data.
    - history_manager (HistoryManager): The manager handling user history data.
    - server (Server): The server handling REST requests.
    - menu_manager (MenuManager): The manager handling menus used for interactions between the Telegram bot and chats.
    - keep_alive_thread (threading.Thread):
      The thread used by the server to ping itself. Used to keep deployment on Render alive.
    - bot_polling_thread (threading.Thread): The thread used by the bot to poll for messages.
    - server_thread (threading.Thread): The thread used by the server to handle REST requests.
    - studios_manager_thread (threading.Thread):
      The thread used by the schedule manager to handle retrieving of schedules.
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
      format="%(asctime)s %(filename)s:%(lineno)d [Thread-%(thread)d][%(levelname)-1s] %(message)s",
      level=logging.INFO,
      datefmt="%d-%m-%Y %H:%M:%S")

    bot_token = os.environ.get("BOT_TOKEN")
    self.bot = telebot.TeleBot(token=bot_token)
    start_command = telebot.types.BotCommand(command="start", description="Check schedules")
    nerd_command = telebot.types.BotCommand(command="nerd", description="Nerd mode")
    instructors_command = telebot.types.BotCommand(command="instructors", description="Show list of instructors")
    self.bot.set_my_commands(commands=[start_command, nerd_command, instructors_command])

    self.chat_manager = ChatManager(bot=self.bot)
    self.keyboard_manager = KeyboardManager()
    self.studios_manager = StudiosManager(logger=self.logger)
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

    # Setup threads
    self.stop_event = threading.Event()
    self.keep_alive_thread = threading.Thread(target=self.keep_alive, daemon=True)
    self.bot_polling_thread = threading.Thread(target=self.start_bot_polling)
    self.server_thread = threading.Thread(target=self.server.start_server, daemon=True)
    self.studios_manager_thread = threading.Thread(
      target=self.studios_manager.schedule_update_cached_result_data,
      daemon=True,
    )

  def keep_alive(self) -> None:
    """
    Periodically pings server. Used to keep deployment on Render alive.
    Scheduled runs is triggered in main thread.
    """
    schedule.every(10).minutes.do(job_func=self.server.ping_self)

  def start_bot_polling(self) -> None:
    """
    Starts the TeleBot's polling mechanism to listen for messages and callback queries.
    """
    self.logger.info("Starting bot polling...")
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
    # Register signal handlers
    signal.signal(signalnum=signal.SIGTERM, handler=self.shutdown)
    signal.signal(signalnum=signal.SIGINT, handler=self.shutdown)

    # Load existing history
    self.history_manager.start()

    # Start schedule manager to get current schedule and store in cache
    self.studios_manager.start()

    # Start threads
    self.logger.info("Starting threads...")
    self.server_thread.start()
    self.keep_alive_thread.start()
    self.studios_manager_thread.start()
    self.bot_polling_thread.start()
    self.logger.info("Bot started!")

    # Keep the main thread alive
    while not self.stop_event.is_set():
      schedule.run_pending()
      time.sleep(1)
