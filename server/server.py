"""
server.py
Author: https://github.com/SQ77
Description: This file defines the Server class which is the main handler for REST API requests.
"""
from flask import Flask, request
import logging
import os
import requests
import telebot

class Server:
  """
  A simple Flask server with basic health check capabilities.

  Attributes:
    - app (Flask): The Flask application instance.
    - logger (logging.Logger): Logger for logging messages.
    - bot (telebot.TeleBot): The Telegram bot instance.
    - base_url (str): Base URL that the Server will be listening on.
    - port (int): Port that the Server will be listening on.
    - health_check_url (str): URL used for health check requests.
  """

  def __init__(
    self,
    logger: logging.Logger,
    bot: telebot.TeleBot,
    base_url: str,
    port: int,
    webhook_path: str,
  ) -> None:
    """
    Initializes the Server instance. Sets up endpoints, and configures logging.

    Args:
      - logger (logging.Logger): Logger for logging messages.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - base_url (str): Base URL that the Server will be listening on.
      - webhook_path (str): The route for the Telegram bot webhook requests.
    """
    self.app = Flask(__name__)
    self.logger = logger
    self.bot = bot
    self.base_url = base_url
    self.port = port
    self.health_check_url = f"{self.base_url}/health"

    # Disable debug and info logs to prevent flooding logs with healthcheck requests
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.WARNING)

    # Initialize routes to listen on
    self.setup_routes(webhook_path=webhook_path)

  def setup_routes(self, webhook_path: str) -> None:
    """
    Sets up the Flask routes for the server.

    Args:
      - webhook_path (str): The route for the Telegram bot webhook requests.
    """
    @self.app.route("/")
    def home():
      """
      Home route to indicate that the server is running.
      """
      return "Server is running"

    @self.app.route("/health", methods=["GET"])
    def health_check():
      """
      Health check route to verify server status.
      """
      return "OK", 200

    @self.app.route(f"/{webhook_path}", methods=["POST"])
    def webhook():
      """
      Webhook route to receive updates for the Telegram bot.
      """
      update = request.get_json()
      if update:
        self.bot.process_new_updates([telebot.types.Update.de_json(update)])
      return "OK", 200

  def ping_self(self) -> None:
    """
    Used to keep deployment on Render alive. The application is
    spun down if there are no external requests for 15 minutes.
    """
    try:
      response = requests.get(url=self.health_check_url)
      if response.status_code == 200:
        self.logger.info(f"Successfully pinged self {self.health_check_url}.")
      else:
        self.logger.warning(f"Unexpected response from server: {response.status_code}")
    except requests.exceptions.RequestException as e:
      self.logger.error(f"Failed to reach self: {e}")

  def start_server(self) -> None:
    """
    Starts the Flask server and defines the health check URL.
    """
    self.logger.info(f"Starting server on {self.base_url}")
    self.app.run(host="0.0.0.0", port=self.port)
