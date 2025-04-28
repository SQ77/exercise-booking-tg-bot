"""
history_manager.py
Author: https://github.com/lendrixxx
Description:
  This file defines the HistoryManager class which is the main handler for
  saving the history of interactions between the Telegram bot and the chats it is being used in.
"""

import logging
import os
import time


class HistoryManager:
    """
    Manages history data and interactions between the Telegram bot and users. This class
    handles saving interactions between the Telegram bot and users.

    Attributes:
      - logger (logging.Logger): Logger for logging messages.
      - file_path (str): Full path of history file to save to.
      - headers (list[str]): List of headers of data to save.

    """

    logger: logging.Logger
    file_path: str
    headers: list[str]

    def __init__(self, logger: logging.Logger) -> None:
        """
        Initializes the HistoryManager instance.

        Args:
          - logger (logging.Logger): The Logger for logging messages.

        """
        self.logger = logger
        self.file_path = "booking-bot-history.csv"
        self.headers = ["timestamp", "user_id", "chat_id", "username", "first_name", "last_name", "command"]

    def start(self) -> None:
        """
        Initializes the history file.

        If there is an existing file, check if the headers matches the required headers.
        If an existing file has mismatched headers, it renames the old file and creates
        a new one.

        """
        if not os.path.exists(self.file_path):
            self.logger.info(f"History file {self.file_path} not found. Creating new file...")
            file = open(self.file_path, "w")
            file.write(",".join(self.headers))
            file.write("\n")
            file.close()
            return

        self.logger.info(f"Found existing history file {self.file_path}. Loading contents...")
        file = open(self.file_path, "r")
        existing_headers = []
        existing_headers = file.readline().strip("\n").split(",")
        file.close()
        if existing_headers != self.headers:
            rename_file_path = f"booking-bot-history-{int(time.time())}.csv"
            self.logger.warning(
                f"Existing headers do not match current headers. Existing: {existing_headers}, "
                f"Current: {self.headers}. Renaming existing file to {rename_file_path}..."
            )
            os.rename(self.file_path, rename_file_path)
            self.start()
            return

    def add(
        self,
        timestamp: int,
        user_id: int,
        chat_id: int,
        username: str,
        first_name: str,
        last_name: str,
        command: str,
    ) -> None:
        """
        Adds a new interaction record to the history file.

        Args:
          - timestamp (int): The timestamp of the interaction.
          - user_id (int): The ID of the Telegram user where the interaction occurred.
          - chat_id (int): The ID of the chat where the interaction occurred.
          - username (str): The username of the user.
          - first_name (str): The first name of the user.
          - last_name (str): The last name of the user.
          - command (str): The command issued by the user.

        """
        self.logger.info(
            f"New request - user_id: {user_id}, chat_id: {chat_id}, username: {username}, "
            f"first_name: {first_name}, last_name: {last_name}, command: {command}"
        )

        file = open(self.file_path, "a")
        file.write(f"{timestamp}, {user_id}, {chat_id}, {username}, {first_name}, {last_name}, {command}\n")
        file.close()
