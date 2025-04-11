"""
main_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to the main page.
"""

import telebot

from chat.chat_manager import ChatManager
from chat.keyboard_manager import KeyboardManager


def main_page_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles the callback query for the main page.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    main_page_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)


def main_page_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles the main page interaction, displaying the schedule and options for filtering
    by studio, instructor, week, day, time, and class name.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    text = "*Schedule to check*\n"
    text += query_data.get_query_str(
        include_studio=True,
        include_instructors=True,
        include_weeks=True,
        include_days=True,
        include_time=True,
        include_class_name_filter=True,
    )

    chat_manager.send_prompt(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard_manager.get_main_page_keyboard(),
        delete_sent_msg_in_future=True,
    )
