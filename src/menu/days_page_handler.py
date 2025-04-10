"""
days_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to selecting days for class schedules.
"""

from copy import copy

from common.data import SORTED_DAYS
from menu.main_page_handler import main_page_handler


def days_page_callback_query_handler(
    query: "telebot.types.CallbackQuery",
    bot: "telebot.TeleBot",
    chat_manager: "ChatManager",
    keyboard_manager: "KeyboardManager",
) -> None:
    """
    Handles the callback query when the step to select day(s) is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data_dict = eval(query.data)
    selected_day = query_data_dict["days"]
    if selected_day == "None":
        chat_manager.update_query_data_days(chat_id=query.message.chat.id, days=[])
    elif selected_day == "All":
        chat_manager.update_query_data_days(chat_id=query.message.chat.id, days=copy(SORTED_DAYS))
    else:
        query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
        if selected_day in query_data.days:
            query_data.days.remove(selected_day)
            chat_manager.update_query_data_days(chat_id=query.message.chat.id, days=query_data.days)
        else:
            query_data.days.append(selected_day)
            query_data.days = sorted(query_data.days, key=SORTED_DAYS.index)
            chat_manager.update_query_data_days(chat_id=query.message.chat.id, days=query_data.days)

    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    text = "*Currently selected day(s)*\n"
    text += query_data.get_query_str(include_days=True)

    days_selection_message = chat_manager.get_days_selection_message(chat_id=query.message.chat.id)
    bot.edit_message_text(
        chat_id=days_selection_message.chat.id,
        message_id=days_selection_message.id,
        text=text,
        reply_markup=keyboard_manager.get_days_keyboard(query=query_data),
        parse_mode="Markdown",
    )


def days_selection_callback_query_handler(
    query: "telebot.types.CallbackQuery",
    chat_manager: "ChatManager",
    keyboard_manager: "KeyboardManager",
) -> None:
    """
    Handles callback queries for selecting the days selection page.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    days_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)


def days_selection_handler(
    message: "telebot.types.Message",
    chat_manager: "ChatManager",
    keyboard_manager: "KeyboardManager",
) -> None:
    """
    Displays the days selection prompt and updates the days selection message of the
    chat.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    text = "*Currently selected day(s)*\n"
    text += query_data.get_query_str(include_days=True)

    sent_msg = chat_manager.send_prompt(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard_manager.get_days_keyboard(query=query_data),
        delete_sent_msg_in_future=True,
    )
    chat_manager.update_days_selection_message(chat_id=message.chat.id, days_selection_message=sent_msg)


def days_next_callback_query_handler(
    query: "telebot.types.CallbackQuery",
    chat_manager: "ChatManager",
    keyboard_manager: "KeyboardManager",
) -> None:
    """
    Handles the callback query when the user proceeds to the next step after selecting
    the day(s). If no day(s) are selected, returns to the days selection page.
    Otherwise, proceeds back to the main page.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    if len(query_data.days) == 0:
        text = "No day(s) selected. Please select the day(s) to get schedule for"
        chat_manager.send_prompt(
            chat_id=query.message.chat.id,
            text=text,
            reply_markup=None,
            delete_sent_msg_in_future=False,
        )
        days_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
        return

    main_page_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
