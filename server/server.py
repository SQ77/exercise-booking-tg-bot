"""
server.py
Author: https://github.com/SQ77
Description: This file defines the Server class which is the main handler for REST API requests.
"""
from flask import Flask
import logging
import os
import requests

class Server:
  """
  A simple Flask server with basic health check capabilities.

  Attributes:
    app (Flask): The Flask application instance.
    logger (logging.Logger): Logger for logging messages.
    health_check_url (str): URL used for health check requests.
  """

  def __init__(self, logger: logging.Logger) -> None:
    """
    Initializes the Server instance. Sets up endpoints, and configures logging.

    Args:
      logger (logging.Logger): Logger for logging messages.
    """
    self.app = Flask(__name__)
    self.logger = logger

    # Disable debug and info logs to prevent flooding logs with healthcheck requests.
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.WARNING)
    self.setup_routes()

  def setup_routes(self) -> None:
    """
    Sets up the Flask routes for the server.
    """
    @self.app.route("/")
    def home():
      """
      Home route to indicate that the server is running.
      """
      return "Dummy Server is running"

    @self.app.route("/health", methods=["GET"])
    def health_check():
      """
      Health check route to verify server status.
      """
      return "OK", 200

  def ping_self(self) -> None:
    """
    Used to keep deployment on Render alive. The application is
    spun down if there are no external requests for 15 minutes.
    """
    try:
      response = requests.get(url=self.health_check_url)
      if response.status_code == 200:
        self.logger.info(f"Successfully pinged the dummy server {self.health_check_url}.")
      else:
        self.logger.warning(f"Unexpected response from server: {response.status_code}")
    except requests.exceptions.RequestException as e:
      self.logger.error(f"Failed to reach dummy server: {e}")

  def start_server(self) -> None:
    """
    Starts the Flask server and defines the health check URL.
    """
    base_url = f"{os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:5000')}"
    self.health_check_url = f"{base_url}/health"
    self.logger.info(f"Starting server on {base_url}")
    self.app.run(host="0.0.0.0", port=5000)
