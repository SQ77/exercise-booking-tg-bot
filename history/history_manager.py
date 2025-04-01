import os
import time

class HistoryManager:
  def __init__(self, logger: "logging.Logger") -> None:
    self.logger = logger
    self.file_path = "booking-bot-history.csv"
    self.headers = ["timestamp", "user_id", "chat_id", "username", "first_name", "last_name", "command"]

  def start(self) -> None:
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

  def add(self, timestamp: int, user_id: int, chat_id: int, username: str, first_name: str, last_name: str, command: str) -> None:
    self.logger.info(f"New request - user_id: {user_id}, chat_id: {chat_id}, username: {username}, first_name: {first_name}, last_name: {last_name}, command: {command}")
    with open(self.file_path, "a") as file:
      file.write(f"{timestamp}, {user_id}, {chat_id}, {username}, {first_name}, {last_name}, {command}\n")
      file.close()
