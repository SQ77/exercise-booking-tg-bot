"""
instructors_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to selecting instructors for class schedules.
"""

import time

import telebot

from chat.chat_manager import ChatManager
from chat.keyboard_manager import KeyboardManager
from common.studio_type import StudioType
from history.history_manager import HistoryManager
from menu.main_page_handler import main_page_handler
from studios.studios_manager import StudiosManager


def instructors_message_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    history_manager: HistoryManager,
    studios_manager: StudiosManager,
) -> None:
    """
    Handles the request to display the names of instructors for all the studios.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - history_manager (HistoryManager): The manager handling user history data.
      - studios_manager (StudiosManager): The manager handling studios data.

    """
    history_manager.add(
        timestamp=int(time.time()),
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        command="instructors",
    )
    text = "*Rev Instructors:* " + ", ".join(studios_manager.studios["Rev"].get_instructor_names()) + "\n\n"
    text += "*Barrys Instructors:* " + ", ".join(studios_manager.studios["Barrys"].get_instructor_names()) + "\n\n"
    text += "*Absolute Instructors:* " + ", ".join(studios_manager.studios["Absolute"].get_instructor_names()) + "\n\n"
    text += "*Ally Instructors:* " + ", ".join(studios_manager.studios["Ally"].get_instructor_names()) + "\n\n"
    text += "*Anarchy Instructors:* " + ", ".join(studios_manager.studios["Anarchy"].get_instructor_names()) + "\n\n"

    chat_manager.add_message_id_to_delete(chat_id=message.chat.id, message_id=message.id)
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)


def instructors_selection_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles the callback query when the step to select instructors is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    instructors_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)


def show_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    studios_manager: StudiosManager,
) -> None:
    """
    Handles the callback query when the step to show instructors is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - studios_manager (StudiosManager): The manager handling studios data.

    """
    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    text = ""
    if StudioType.Rev in query_data.studios:
        text += "*Rev Instructors:* " + ", ".join(studios_manager.studios["Rev"].get_instructor_names()) + "\n\n"
    if StudioType.Barrys in query_data.studios:
        text += "*Barrys Instructors:* " + ", ".join(studios_manager.studios["Barrys"].get_instructor_names()) + "\n\n"
    if StudioType.AbsoluteSpin in query_data.studios or StudioType.AbsolutePilates in query_data.studios:
        text += (
            "*Absolute Instructors:* " + ", ".join(studios_manager.studios["Absolute"].get_instructor_names()) + "\n\n"
        )
    if StudioType.AllySpin in query_data.studios or StudioType.AllyPilates in query_data.studios:
        text += "*Ally Instructors:* " + ", ".join(studios_manager.studios["Ally"].get_instructor_names()) + "\n\n"
    if StudioType.AllyRecovery in query_data.studios:
        text += "No instructors for Ally (Recovery)\n\n"
    if StudioType.Anarchy in query_data.studios:
        text += (
            "*Anarchy Instructors:* " + ", ".join(studios_manager.studios["Anarchy"].get_instructor_names()) + "\n\n"
        )

    chat_manager.send_prompt(
        chat_id=query.message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
    )
    instructors_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)


def rev_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter rev instructors is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\ne.g.: *chloe*, *jerlyn*, *zai*\n"
        "Enter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=StudioType.Rev)
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def barrys_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter barrys instructors is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\ne.g.: *ria*, *gino*\nEnter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=StudioType.Barrys)
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def absolute_spin_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter absolute (spin) instructors is
    triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\ne.g.: *chin*, *ria*\nEnter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=StudioType.AbsoluteSpin)
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def absolute_pilates_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter absolute (pilates) instructors is
    triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\n"
        "e.g.: *daniella*, *vnex*\nEnter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(
        chat_id=query.message.chat.id,
        current_studio=StudioType.AbsolutePilates,
    )
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def ally_spin_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter ally (spin) instructors is
    triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\n"
        "e.g.: *samuel*, *jasper*\nEnter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=StudioType.AllySpin)
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def ally_pilates_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter ally (pilates) instructors is
    triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\n"
        "e.g.: *candice*, *ruth*\nEnter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=StudioType.AllyPilates)
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def anarchy_instructors_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    bot: telebot.TeleBot,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles the callback query when the step to enter anarchy instructors is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    text = (
        "Enter instructor names separated by a comma\n"
        "e.g.: *lyon*, *isabelle*\nEnter '*all*' to check for all instructors"
    )
    chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=StudioType.Anarchy)
    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=instructors_input_handler,
        chat_manager=chat_manager,
        keyboard_manager=keyboard_manager,
        instructorid_map=instructorid_map,
    )


def instructors_input_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
    instructorid_map: dict[str, str],
) -> None:
    """
    Handles user input for instructor names, validating them against the instructor map.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
      - instructorid_map (dict[str, str]): Dictionary of instructor names and IDs

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    updated_instructors_list = [x.strip() for x in message.text.lower().split(",")]
    if "all" in updated_instructors_list:
        query_data.studios[query_data.current_studio].instructors = ["All"]
        chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
    else:
        invalid_instructors = []
        if "/" in updated_instructors_list:  # Some names contain "/" which should not be considered as a valid name
            invalid_instructors.append("/")
            updated_instructors_list.remove("/")

        for instructor in updated_instructors_list:
            instructor_in_map = (
                any(instructor in instructor_in_map.split(" ") for instructor_in_map in instructorid_map)
                or any(instructor == instructor_in_map for instructor_in_map in instructorid_map)
                or any(instructor == instructor_in_map.split(".")[0] for instructor_in_map in instructorid_map)
            )
            if not instructor_in_map:
                invalid_instructors.append(instructor)

        if len(invalid_instructors) > 0:
            updated_instructors_list = [
                instructor for instructor in updated_instructors_list if instructor not in invalid_instructors
            ]
            text = f"Failed to find instructor(s): {', '.join(invalid_instructors)}"
            chat_manager.send_prompt(
                chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
            )

        if len(updated_instructors_list) > 0:
            query_data.studios[query_data.current_studio].instructors = updated_instructors_list
            chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)

    instructors_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)


def instructors_selection_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Displays the instructors selection prompt.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    if len(query_data.studios) == 0:
        text = "No studio selected. Please select a studio first"
        chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
        main_page_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
        return

    text = "*Currently selected instructor(s)*\n"
    text += query_data.get_query_str(include_instructors=True)

    chat_manager.send_prompt(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard_manager.get_instructors_keyboard(query=query_data),
        delete_sent_msg_in_future=True,
    )
