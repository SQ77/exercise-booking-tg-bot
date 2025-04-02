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
    - base_url (str): Base URL that the Server will be listening on.
    - webhook_path (str): The route for the Telegram bot webhook requests.
    - bot (telebot.TeleBot): The Telegram bot instance.
    - bot_token (str): The Telegram bot token.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
    - studios_manager (StudiosManager): The manager handling studios data.
    - history_manager (HistoryManager): The manager handling user history data.
    - server (Server): The server handling REST requests.
    - menu_manager (MenuManager): The manager handling menus used for interactions between the Telegram bot and chats.
    - keep_alive_thread (threading.Thread):
      The thread used by the server to ping itself. Used to keep deployment on Render alive.
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

    self.load_env_vars()
    self.bot = telebot.TeleBot(token=self.bot_token)
    start_command = telebot.types.BotCommand(command="start", description="Check schedules")
    nerd_command = telebot.types.BotCommand(command="nerd", description="Nerd mode")
    instructors_command = telebot.types.BotCommand(command="instructors", description="Show list of instructors")
    self.bot.set_my_commands(commands=[start_command, nerd_command, instructors_command])

    self.chat_manager = ChatManager(bot=self.bot)
    self.keyboard_manager = KeyboardManager()
    self.studios_manager = StudiosManager(logger=self.logger, rev_security_token=self.rev_security_token)
    self.history_manager = HistoryManager(logger=self.logger)
    self.server = Server(
      logger=self.logger,
      base_url=self.base_url,
      port=self.server_port,
      bot=self.bot,
      webhook_path=self.webhook_path,
    )
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
    self.server_thread = threading.Thread(target=self.server.start_server, daemon=True)
    self.studios_manager_thread = threading.Thread(
      target=self.studios_manager.schedule_update_cached_result_data,
      daemon=True,
    )

  def load_env_vars(self):
    """
    Loads the environment variables to be used for the application.
    Exits the application if a required environment variable could not be loaded.
    """
    loaded_successfully = True
    self.base_url = os.getenv('RENDER_EXTERNAL_URL', os.getenv('TELEGRAM_BOT_EXTERNAL_URL'))
    if self.base_url is None:
      self.logger.error("RENDER_EXTERNAL_URL or TELEGRAM_BOT_EXTERNAL_URL env var required but not set")
      loaded_successfully = False

    self.webhook_path = os.getenv('WEBHOOK_PATH')
    if self.webhook_path is None:
      self.logger.error("WEBHOOK_PATH env var required but not set")
      loaded_successfully = False

    self.bot_token = os.getenv("BOT_TOKEN")
    if self.bot_token is None:
      self.logger.error("BOT_TOKEN env var required but not set")
      loaded_successfully = False

    self.rev_security_token = os.getenv("BOOKING_BOT_REV_SECURITY_TOKEN")
    if self.rev_security_token is None:
      self.logger.error("BOOKING_BOT_REV_SECURITY_TOKEN env var required but not set")
      loaded_successfully = False

    self.server_port = os.getenv("PORT")
    if self.server_port is None:
      # PORT env var not mandatory, default to 80 if not found
      self.logger.warning("PORT env var not found. Defaulting to 80")
      self.server_port = 80

    if not loaded_successfully:
      self.logger.error("Failed to initialize app. Exiting...")
      exit(1)

  def set_webhook(self):
    """
    Sets the webhook url for the Telegram bot.
    """
    webhook_url = f"{self.base_url}/{self.webhook_path}"
    self.bot.set_webhook(url=webhook_url)
    self.logger.info(f"Webhook for Telegram bot successfully set!")

  def keep_alive(self) -> None:
    """
    Periodically pings server. Used to keep deployment on Render alive.
    Scheduled runs is triggered in main thread.
    """
    schedule.every(10).minutes.do(job_func=self.server.ping_self)

  def shutdown(self, _: int, __: "types.FrameType") -> None:
    """
    Gracefully shuts down the bot and background threads.

    Args:
      - _ (int): Signal number received, but not used in this function.
      - __ (types.FrameType): Current stack frame at the time of signal reception, but not used in this function.
    """
    self.logger.info("Received termination signal. Shutting down application...")

    # Signal threads to stop
    self.stop_event.set()

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

    # Initialize webhook for Telegram bot
    self.set_webhook()

    # Start threads
    self.logger.info("Starting threads...")
    self.server_thread.start()
    self.keep_alive_thread.start()
    self.studios_manager_thread.start()
    self.logger.info("Bot started!")

    # Keep the main thread alive
    while not self.stop_event.is_set():
      schedule.run_pending()
      time.sleep(1)
