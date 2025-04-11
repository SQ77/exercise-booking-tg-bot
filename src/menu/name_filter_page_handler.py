"""
name_filter_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to entering class name filters for class schedules.
"""

import telebot

from chat.chat_manager import ChatManager
from chat.keyboard_manager import KeyboardManager


def class_name_filter_selection_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles the callback query when the step to enter a class name filter is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    class_name_filter_selection_handler(
        message=query.message,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
    )


def class_name_filter_selection_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Displays the current class name filter and provides options to set or reset the
    filter.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    text = "*Current filter*\n"
    text += query_data.get_query_str(include_class_name_filter=True)

    chat_manager.send_prompt(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard_manager.get_class_name_filter_keyboard(),
        delete_sent_msg_in_future=True,
    )


def class_name_filter_set_callback_query_handler(
    query: telebot.types.CallbackQuery,
    bot: telebot.TeleBot,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Initiates the process of setting a class name filter by prompting the user for
    input.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    text = "Enter name of class to filter (non-case sensitive)\ne.g. *essential*"
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=class_name_filter_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
    )


def class_name_filter_input_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Processes the user's input for setting a class name filter and updates the query
    data.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    query_data.class_name_filter = message.text
    class_name_filter_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)


def class_name_filter_reset_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Resets the class name filter to an empty value.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    query_data.class_name_filter = ""
    class_name_filter_selection_handler(
        message=query.message,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
    )
