"""
nerd_message_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to nerd mode.
"""

import logging
import time
from datetime import datetime

import telebot

from chat.chat_manager import ChatManager
from common.data import SORTED_DAYS
from common.query_data import QueryData
from common.result_data import ResultData
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from history.history_manager import HistoryManager
from studios.studios_manager import StudiosManager


def nerd_message_handler(
    message: telebot.types.Message,
    logger: logging.Logger,
    bot: telebot.TeleBot,
    chat_manager: ChatManager,
    history_manager: HistoryManager,
    studios_manager: StudiosManager,
    full_result_data: ResultData,
) -> None:
    """
    Initiates nerd mode and prompts the user for structured query input.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - logger (logging.Logger): Logger for logging messages.
      - bot (telebot.TeleBot): The instance of the Telegram bot.
      - chat_manager (ChatManager): The manager handling chat data.
      - history_manager (HistoryManager): The manager handling user history data.
      - studios_manager (StudiosManager): The manager handling studios data.
      - full_result_data (ResultData): The schedule data of all the available classes.

    """
    history_manager.add(
        timestamp=int(time.time()),
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        command="nerd",
    )
    text = (
        "Welcome to nerd mode 🤓\n"
        "\n"
        "*Enter your query in the following format:*\n"
        "Studio name\n"
        "Studio locations (comma separated)\n"
        "Instructor names (comma separated)\n"
        "(Repeat above for multiple studios)\n"
        "Weeks\n"
        "Days\n"
        "Timeslots (comma separated. enter 'nil' to ignore filters)\n"
        "Class Name Filter (enter 'nil' to ignore filters)\n"
        "\n"
        "*Studio names*: rev, barrys, absolute (spin), absolute (pilates), ally (spin), ally (pilates)\n"
        "*Studio locations*: orchard, tjpg, bugis, raffles, centrepoint, i12, "
        "millenia walk, star vista, great world, cross street\n"
        "*Instructors*: Use /instructors for list of instructors\n"
        "\n"
        "*e.g.*\n"
        "`rev\n"
        "bugis, orchard\n"
        "chloe, zai\n"
        "absolute (spin)\n"
        "raffles\n"
        "ria\n"
        "2\n"
        "monday, wednesday, saturday\n"
        "0700-0900, 1300-1500, 1800-2000\n"
        "essential\n`"
    )

    chat_manager.add_message_id_to_delete(chat_id=message.chat.id, message_id=message.id)
    sent_msg = chat_manager.send_prompt(
        chat_id=message.chat.id,
        text=text,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )
    bot.register_next_step_handler(
        message=sent_msg,
        callback=nerd_input_handler,
        logger=logger,
        chat_manager=chat_manager,
        studios_manager=studios_manager,
        full_result_data=full_result_data,
    )


def nerd_input_handler(
    message: telebot.types.Message,
    logger: logging.Logger,
    chat_manager: ChatManager,
    studios_manager: StudiosManager,
    full_result_data: ResultData,
) -> None:
    """
    Processes the user's input, validates it, and retrieves filtered results. See
    nerd_handler function header for expected message format.

    Args:
      - message (telebot.types.Message): The message object containing user interaction data.
      - logger (logging.Logger): Logger for logging messages.
      - chat_manager (ChatManager): The manager handling chat data.
      - studios_manager (StudiosManager): The manager handling studios data.
      - full_result_data (ResultData): The schedule data of all the available classes.

    """
    input_str_list = message.text.splitlines()

    # Weeks, days, timeslots, and class name filter = 4 items
    # Remaining items should be divisible by 3 (studio name, locations, instructors)
    if len(input_str_list) < 7 or (len(input_str_list) - 4) % 3 != 0:
        text = "Failed to handle query. Unexpected format received."
        chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
        return

    # Loop through studios
    query = QueryData(
        studios=None, current_studio=StudioType.Null, weeks=0, days=[], start_times=[], class_name_filter=""
    )
    current_studio = StudioType.Null
    current_studio_locations = []
    for index, input_str in enumerate(input_str_list[:-4]):
        step = index % 3
        if step == 0:  # Studio name
            found_studio = False
            for studio in StudioType:
                if input_str.lower() == studio.value.lower():
                    current_studio = studio
                    found_studio = True
                    break
            if not found_studio:
                text = f"Failed to handle query. Unexpected studio name '{input_str}'"
                chat_manager.send_prompt(
                    chat_id=message.chat.id,
                    text=text,
                    reply_markup=None,
                    delete_sent_msg_in_future=False,
                )
                return
        elif step == 1:  # Studio locations
            selected_locations = [x.strip() for x in input_str.split(",")]
            for selected_location in selected_locations:
                found_location = False
                for location in StudioLocation:
                    if selected_location.lower() == location.value.lower():
                        current_studio_locations.append(location)
                        found_location = True
                        break
                if not found_location:
                    text = f"Failed to handle query. Unexpected studio name '{selected_location}'"
                    chat_manager.send_prompt(
                        chat_id=message.chat.id,
                        text=text,
                        reply_markup=None,
                        delete_sent_msg_in_future=False,
                    )
                    return
        elif step == 2:  # Studio instructors
            instructor_list = []
            if current_studio == StudioType.Rev:
                instructor_list = studios_manager.studios["Rev"].get_instructor_names()
            elif current_studio == StudioType.Barrys:
                instructor_list = studios_manager.studios["Barrys"].get_instructor_names()
            elif current_studio == StudioType.AbsolutePilates or current_studio == StudioType.AbsoluteSpin:
                instructor_list = studios_manager.studios["Absolute"].get_instructor_names()
            elif (
                current_studio == StudioType.AllyPilates
                or current_studio == StudioType.AllySpin
                or current_studio == StudioType.AllyRecovery
            ):
                instructor_list = studios_manager.studios["Ally"].get_instructor_names()
            elif current_studio == StudioType.Anarchy:
                instructor_list = studios_manager.studios["Anarchy"].get_instructor_names()

            selected_instructors = [x.strip().lower() for x in input_str.split(",")]
            invalid_instructors = []
            if "all" in selected_instructors:
                selected_instructors = ["All"]
            else:
                for instructor in selected_instructors:
                    found_instructor = (
                        any(instructor in instructor_in_list.split(" ") for instructor_in_list in instructor_list)
                        or any(instructor == instructor_in_list for instructor_in_list in instructor_list)
                        or any(instructor == instructor_in_list.split(".")[0] for instructor_in_list in instructor_list)
                    )
                    if not found_instructor:
                        invalid_instructors.append(instructor)

            if len(invalid_instructors) > 0:
                selected_instructors = [
                    instructor for instructor in selected_instructors if instructor not in invalid_instructors
                ]
                text = f"Failed to find instructor(s): {', '.join(invalid_instructors)}"
                chat_manager.send_prompt(
                    chat_id=message.chat.id,
                    text=text,
                    reply_markup=None,
                    delete_sent_msg_in_future=False,
                )

            if len(selected_instructors) == 0:
                text = f"Failed to handle query. No instructor selected for {current_studio.value}"
                chat_manager.send_prompt(
                    chat_id=message.chat.id,
                    text=text,
                    reply_markup=None,
                    delete_sent_msg_in_future=False,
                )
                return

            query.studios[current_studio] = StudioData(
                locations=current_studio_locations, instructors=selected_instructors
            )

    # Get number of weeks
    try:
        query.weeks = int(input_str_list[-4])
    except Exception as e:
        text = f"Failed to handle query. Invalid input for 'weeks'. Expected number, got {input_str_list[-2]} - {e}"
        chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
        return

    # Get list of days
    query.days = [x.strip().capitalize() for x in input_str_list[-3].split(",")]
    if "All" in query.days:
        query.days = ["All"]
    else:
        for selected_day in query.days:
            if selected_day.capitalize() not in SORTED_DAYS:
                text = f"Failed to handle query. Invalid input for 'days'. Unknown day {selected_day}"
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

    # Get timeslots
    timeslots_without_whitespace = "".join(input_str_list[-2].split())
    timeslots = timeslots_without_whitespace.split(",")
    if "nil" not in timeslots:
        for timeslot in timeslots:
            timings = timeslot.split("-")
            if len(timings) != 2:
                text = f"Failed to handle query. Invalid input for 'timeslots'. '{timeslot}' is not a valid timeslot"
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            start_time_str = timings[0]
            end_time_str = timings[1]

            if len(start_time_str) != 4:
                text = (
                    f"Failed to handle query. Invalid input for 'timeslots'. Start time '{start_time_str}' is not valid"
                )
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            if len(end_time_str) != 4:
                text = f"Failed to handle query. Invalid input for 'timeslots'. End time '{end_time_str}' is not valid"
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            try:
                start_time = datetime.strptime(start_time_str, "%H%M")
            except Exception as e:
                logger.warning(f"Invalid time '{start_time_str}' entered: {str(e)}")
                text = f"Invalid time '{start_time_str}' entered. Please enter time in 24 hour format"
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            try:
                end_time = datetime.strptime(end_time_str, "%H%M")
            except Exception as e:
                logger.warning(f"Invalid time '{end_time_str}' entered: {str(e)}")
                text = f"Invalid time '{end_time_str}' entered. Please enter time in 24 hour format"
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            if end_time < start_time:
                text = (
                    f"Failed to handle query. Invalid input for 'timeslots'. "
                    f"Start time '{start_time_str}' is later than end time '{end_time_str}'"
                )
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            # Start time from should be at least one minute before
            # existing start time or greater than or equal existing end time
            is_valid_start_time = True
            for existing_start_time, existing_end_time in query.start_times:
                at_least_one_minute_before_existing_start_time = (
                    start_time.hour < existing_start_time.hour
                    or start_time.hour == existing_start_time.hour
                    and start_time.minute < existing_start_time.minute
                )
                greater_than_or_equal_existing_end_time = start_time >= existing_end_time
                if not at_least_one_minute_before_existing_start_time and not greater_than_or_equal_existing_end_time:
                    conflicting_start_time_str = existing_start_time.strftime("%H%M")
                    conflicting_end_time_str = existing_end_time.strftime("%H%M")
                    is_valid_start_time = False
                    break

                # Edge case where existing timeslot start time and end time are the same
                if (
                    existing_start_time.hour == existing_end_time.hour
                    and existing_start_time.minute == existing_end_time.minute
                ):
                    if start_time.hour == existing_start_time.hour and start_time.minute == existing_start_time.minute:
                        conflicting_start_time_str = existing_start_time.strftime("%H%M")
                        conflicting_end_time_str = existing_end_time.strftime("%H%M")
                        is_valid_start_time = False
                        break

            if not is_valid_start_time:
                text = (
                    f"Start time '{start_time_str}' conflicts with existing timeslot "
                    f"'{conflicting_start_time_str} - {conflicting_end_time_str}'"
                )
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            # Start time to should be less than or equal to existing start time or greater than existing end time
            is_valid_end_time = True
            for existing_start_time, existing_end_time in query.start_times:
                less_than_or_equal_existing_start_time = end_time <= existing_start_time
                greater_than_existing_end_time = end_time > existing_end_time
                if not less_than_or_equal_existing_start_time and not greater_than_existing_end_time:
                    conflicting_start_time_str = existing_start_time.strftime("%H%M")
                    conflicting_end_time_str = existing_end_time.strftime("%H%M")
                    is_valid_end_time = False
                    break

                # If end time is greater than existing end time, start time must also be greater than existing end time
                if greater_than_existing_end_time:
                    if start_time < existing_end_time:
                        conflicting_start_time_str = existing_start_time.strftime("%H%M")
                        conflicting_end_time_str = existing_end_time.strftime("%H%M")
                        text = (
                            f"Time range '{start_time_str} - {end_time_str}' conflicts with existing timeslot "
                            f"'{conflicting_start_time_str} - {conflicting_end_time_str}'"
                        )
                        chat_manager.send_prompt(
                            chat_id=message.chat.id,
                            text=text,
                            reply_markup=None,
                            delete_sent_msg_in_future=False,
                        )
                        return

            if not is_valid_end_time:
                text = (
                    f"End time '{end_time_str}' conflicts with existing timeslot "
                    f"'{conflicting_start_time_str} - {conflicting_end_time_str}'"
                )
                chat_manager.send_prompt(
                    chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False
                )
                return

            query.start_times.append((start_time, end_time))
            query.start_times = sorted(query.start_times)

    # Get class name filter
    query.class_name_filter = "" if input_str_list[-1] == "nil" else input_str_list[-1]

    # Get and send results
    result = full_result_data.get_data(query=query)
    schedule_str = result.get_result_str()
    if len(schedule_str) > 4095:
        shortened_message = ""
        for line in schedule_str.splitlines():
            is_new_day = any(day in line for day in SORTED_DAYS) and len(shortened_message) > 0
            max_len_reached = len(shortened_message) + len(line) > 4095
            if is_new_day or max_len_reached:
                chat_manager.send_prompt(
                    chat_id=message.chat.id,
                    text=shortened_message,
                    reply_markup=None,
                    delete_sent_msg_in_future=False,
                )
                shortened_message = line + "\n"
            else:
                shortened_message += line + "\n"

        if len(shortened_message) > 0:
            chat_manager.send_prompt(
                chat_id=message.chat.id,
                text=shortened_message,
                reply_markup=None,
                delete_sent_msg_in_future=False,
            )
    else:
        chat_manager.send_prompt(
            chat_id=message.chat.id,
            text=schedule_str,
            reply_markup=None,
            delete_sent_msg_in_future=False,
        )
