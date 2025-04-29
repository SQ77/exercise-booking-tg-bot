"""
studios_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to selecting studios for class schedules.
"""

from copy import copy

import telebot

from chat.chat_manager import ChatManager
from chat.keyboard_manager import KeyboardManager
from common.data import STUDIO_LOCATIONS_MAP
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


def studios_selection_callback_query_handler(
    query: telebot.types.CallbackQuery,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles the callback query when the step to select studios is triggered.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    text = "*Currently selected studio(s)*\n"
    text += query_data.get_query_str(include_studio=True)

    sent_msg = chat_manager.send_prompt(
        chat_id=query.message.chat.id,
        text=text,
        reply_markup=keyboard_manager.get_studios_keyboard(query=query_data),
        delete_sent_msg_in_future=True,
    )
    chat_manager.update_studios_selection_message(chat_id=query.message.chat.id, studios_selection_message=sent_msg)


def studios_callback_query_handler(
    query: telebot.types.CallbackQuery,
    bot: telebot.TeleBot,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles callback queries for selecting the studios selection page.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data_dict = eval(query.data)
    selected_studio = StudioType[query_data_dict["studios"]]
    if selected_studio == StudioType.Null:
        chat_manager.update_query_data_studios(chat_id=query.message.chat.id, studios={})
    elif selected_studio == StudioType.All:
        chat_manager.update_query_data_select_all_studios(chat_id=query.message.chat.id)
    elif selected_studio == StudioType.Anarchy:
        chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=selected_studio)
        select_location_handler(
            message=query.message,
            selected_studio_location=StudioLocation.Robinson,
            chat_manager=chat_manager,
        )
    else:
        chat_manager.update_query_data_current_studio(chat_id=query.message.chat.id, current_studio=selected_studio)
        locations_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
        return

    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    text = "*Currently selected studio(s)*\n"
    text += query_data.get_query_str(include_studio=True)

    studios_selection_message = chat_manager.get_studios_selection_message(chat_id=query.message.chat.id)
    bot.edit_message_text(
        chat_id=studios_selection_message.chat.id,
        message_id=studios_selection_message.id,
        text=text,
        reply_markup=keyboard_manager.get_studios_keyboard(query=query_data),
        parse_mode="Markdown",
    )


def locations_handler(
    message: telebot.types.Message,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles the step for selecting the studio locations.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    text = "*Currently selected studio(s)*\n"
    text += query_data.get_query_str(include_studio=True)

    sent_msg = chat_manager.send_prompt(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard_manager.get_locations_keyboard(query=query_data),
        delete_sent_msg_in_future=True,
    )
    chat_manager.update_locations_selection_message(chat_id=message.chat.id, locations_selection_message=sent_msg)


def select_location_handler(
    message: telebot.types.Message,
    selected_studio_location: StudioLocation,
    chat_manager: ChatManager,
) -> None:
    """
    Handles the selection of a studio location.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - selected_studio_location (StudioLocation): The selected studio location.
      - chat_manager (ChatManager): The manager handling chat data.

    """
    query_data = chat_manager.get_query_data(chat_id=message.chat.id)
    if selected_studio_location == StudioLocation.Null:
        query_data.studios.pop(query_data.current_studio)
        chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
    elif selected_studio_location == StudioLocation.All:
        if query_data.current_studio not in query_data.studios:
            new_studio = {
                query_data.current_studio: StudioData(locations=copy(STUDIO_LOCATIONS_MAP[query_data.current_studio]))
            }
            query_data.studios = {**query_data.studios, **new_studio}
            chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
        else:
            query_data.studios[query_data.current_studio].locations = copy(
                STUDIO_LOCATIONS_MAP[query_data.current_studio]
            )
            chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
    else:
        if query_data.current_studio not in query_data.studios:
            new_studio = {query_data.current_studio: StudioData(locations=[selected_studio_location])}
            query_data.studios = {**query_data.studios, **new_studio}
            chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
        elif selected_studio_location in query_data.studios[query_data.current_studio].locations:
            query_data.studios[query_data.current_studio].locations.remove(selected_studio_location)
            if len(query_data.studios[query_data.current_studio].locations) == 0:
                query_data.studios.pop(query_data.current_studio)
            chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
        else:
            query_data.studios[query_data.current_studio].locations.append(selected_studio_location)
            chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)


def locations_callback_query_handler(
    query: telebot.types.CallbackQuery,
    bot: telebot.TeleBot,
    chat_manager: ChatManager,
    keyboard_manager: KeyboardManager,
) -> None:
    """
    Handles callback queries for selecting the locations selection page.

    Args:
      - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - chat_manager (ChatManager): The manager handling chat data.
      - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.

    """
    query_data_dict = eval(query.data)
    query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
    select_location_handler(
        message=query.message,
        selected_studio_location=StudioLocation[query_data_dict["location"]],
        chat_manager=chat_manager,
    )
    text = "*Currently selected studio(s)*\n"
    text += query_data.get_query_str(include_studio=True)

    locations_selection_message = chat_manager.get_locations_selection_message(chat_id=query.message.chat.id)
    bot.edit_message_text(
        chat_id=locations_selection_message.chat.id,
        message_id=locations_selection_message.id,
        text=text,
        reply_markup=keyboard_manager.get_locations_keyboard(query=query_data),
        parse_mode="Markdown",
    )
