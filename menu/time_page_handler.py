"""
time_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to entering time filters for class schedules.
"""
import telebot
from datetime import datetime

def time_selection_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to enter a time filter is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  time_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)

def time_selection_handler(
  message: telebot.types.Message,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Displays the current time filters and provides options to add, remove, or reset the filters.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  query_data = chat_manager.get_query_data(chat_id=message.chat.id)
  text = "*Currently selected timings(s)*\n"
  text += query_data.get_query_str(include_time=True)

  chat_manager.send_prompt(
    chat_id=message.chat.id,
    text=text,
    reply_markup=keyboard_manager.get_timeslot_filter_keyboard(),
    delete_sent_msg_in_future=True,
  )

def time_selection_add_callback_query_handler(
  query: telebot.types.CallbackQuery,
  logger: "logging.Logger",
  bot: "telebot.TeleBot",
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to add a time filter is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - logger (logging.Logger): Logger for logging messages.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  start_time_selection_handler(
    message=query.message,
    logger=logger,
    bot=bot,
    chat_manager=chat_manager,
    keyboard_manager=keyboard_manager,
  )

def start_time_selection_handler(
  message: telebot.types.Message,
  logger: "logging.Logger",
  bot: "telebot.TeleBot",
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Initiates the process of setting a time filter by prompting the user for input.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - logger (logging.Logger): Logger for logging messages.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  text = "Enter range of timeslot to check\ne.g. *0700-0830*"
  sent_msg = chat_manager.send_prompt(
    chat_id=message.chat.id,
    text=text,
    reply_markup=None,
    delete_sent_msg_in_future=True,
  )
  bot.register_next_step_handler(
    message=sent_msg,
    callback=timeslot_input_handler,
    logger=logger,
    chat_manager=chat_manager,
    keyboard_manager=keyboard_manager,
  )

def timeslot_input_handler(
  message: telebot.types.Message,
  logger: "logging.Logger",
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Processes the user's input for a timeslot.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - logger (logging.Logger): Logger for logging messages.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  try:
    message_without_whitespace = "".join(message.text.split())
    split_message_without_whitespace = message_without_whitespace.split("-")
    if len(split_message_without_whitespace) != 2:
      raise Exception("Input has invalid format")

    start_time_str = split_message_without_whitespace[0]
    end_time_str = split_message_without_whitespace[1]

    if len(start_time_str) != 4:
      raise Exception("Start time has invalid length")

    if len(end_time_str) != 4:
      raise Exception("End time has invalid length")

    start_time = datetime.strptime(start_time_str, "%H%M")
    end_time = datetime.strptime(end_time_str, "%H%M")
  except Exception as e:
    logger.warning(f"Invalid time '{message.text}' entered: {str(e)}")
    text = f"Invalid timeslot range '{message.text}' entered"
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
    time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
    return

  if end_time < start_time:
    text = (
      f"End time must be later than or equal start time. "
      f"Start time: {start_time.strftime('%H%M')}, End time: {end_time.strftime('%H%M')}"
    )
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
    time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
    return

  query_data = chat_manager.get_query_data(chat_id=message.chat.id)

  # Start time should be at least one minute before existing start time or greater than or equal existing end time
  is_valid_start_time = True
  for existing_start_time, existing_end_time in query_data.start_times:
    at_least_one_minute_before_existing_start_time = (
      start_time.hour < existing_start_time.hour
      or start_time.hour == existing_start_time.hour and start_time.minute < existing_start_time.minute
    )
    greater_than_or_equal_existing_end_time = start_time >= existing_end_time
    if not at_least_one_minute_before_existing_start_time and not greater_than_or_equal_existing_end_time:
      conflicting_start_time_str = existing_start_time.strftime("%H%M")
      conflicting_end_time_str = existing_end_time.strftime("%H%M")
      is_valid_start_time = False
      break

    # Edge case where existing timeslot start time and end time are the same
    if existing_start_time.hour == existing_end_time.hour and existing_start_time.minute == existing_end_time.minute:
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
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
    time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
    return

  # End time should be less than or equal to existing start time or greater than existing end time
  is_valid_end_time = True
  for existing_start_time, existing_end_time in query_data.start_times:
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
        chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
        time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
        return

  if not is_valid_end_time:
    text = (
      f"End time '{end_time_str}' conflicts with existing timeslot "
      f"'{conflicting_start_time_str} - {conflicting_end_time_str}'"
    )
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
    time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
    return

  query_data.start_times.append((start_time, end_time))
  query_data.start_times = sorted(query_data.start_times)
  time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)

def time_selection_remove_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to remove a time filter is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  time_selection_remove_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)

def time_selection_remove_handler(
  message: telebot.types.Message,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to remove a time filter is triggered.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  query_data = chat_manager.get_query_data(chat_id=message.chat.id)
  if len(query_data.start_times) == 0:
    text = "No timeslot to remove"
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
    time_selection_handler(message=message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
  else:
    text = "*Select timeslot to remove*"
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = []
    for start_time, end_time in query_data.start_times:
      start_time_str = start_time.strftime("%H%M")
      end_time_str = end_time.strftime("%H%M")
      remove_timeslot_button = telebot.types.InlineKeyboardButton(
        text=f"{start_time_str} - {end_time_str}",
        callback_data=f"{{'step': 'remove-timeslot', 'start':'{start_time_str}', 'end':'{end_time_str}'}}",
      )
      buttons.append(remove_timeslot_button)
      keyboard.add(buttons[-1])

    back_button = telebot.types.InlineKeyboardButton(
      text="◀️ Back",
      callback_data="{'step': 'time-selection'}",
    )
    keyboard.add(back_button)
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=keyboard, delete_sent_msg_in_future=True)

def time_selection_remove_timeslot_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to remove a timeslot is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  start_time = eval(query.data)["start"]
  end_time = eval(query.data)["end"]
  query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
  query_data.start_times.remove((datetime.strptime(start_time, "%H%M"), datetime.strptime(end_time, "%H%M")))
  time_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)

def time_selection_reset_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to reset the timeslot filter triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
  query_data.start_times = []
  time_selection_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
