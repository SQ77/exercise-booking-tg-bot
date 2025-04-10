"""
start_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to the start message command.
"""

import time

from menu.main_page_handler import main_page_handler


def start_message_handler(
    message: "telebot.types.Message",
    chat_manager: "ChatManager",
    keyboard_manager: "KeyboardManager",
    history_manager: "HistoryManager",
) -> None:
    """
    Handles the request to start the process of retrieving schedules.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - history_manager (HistoryManager): The manager handling user history data.

    """
    history_manager.add(
        timestamp=int(time.time()),
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        command="start",
    )
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=message.chat.id)
    chat_manager.add_message_id_to_delete(chat_id=message.chat.id, message_id=message.id)
    main_page_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
