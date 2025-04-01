"""
instructors_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to selecting instructors for class schedules.
"""
import telebot
import time
from common.studio_type import StudioType
from menu.main_page_handler import main_page_handler

def instructors_message_handler(
  message: telebot.types.Message,
  chat_manager: "ChatManager",
  history_manager: "HistoryManager",
  studios_manager: "StudiosManager",
) -> None:
  """
  Handles the request to display the names of instructors for all the studios.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - history_manager (HistoryManager): The manager handling user history data.
    - studios_manager (StudiosManager): The manager handling studio data.
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
  text = "*Rev Instructors:* " + ", ".join(studios_manager["Rev"].instructor_names) + "\n\n"
  text += "*Barrys Instructors:* " + ", ".join(studios_manager["Barrys"].instructor_names) + "\n\n"
  text += "*Absolute Instructors:* " + ", ".join(studios_manager["Absolute"].instructor_names) + "\n\n"
  text += "*Ally Instructors:* " + ", ".join(studios_manager["Ally"].instructor_names) + "\n\n"
  text += "*Anarchy Instructors:* " + ", ".join(studios_manager["Anarchy"].instructor_names) + "\n\n"

  chat_manager.add_message_id_to_delete(chat_id=message.chat.id, message_id=message.id)
  chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)

def instructors_selection_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
) -> None:
  """
  Handles the callback query when the step to select instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
  """
  query_data_dict = eval(query.data)
  instructors_selection_handler(message=query.message, chat_manager=chat_manager)

def show_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  studios_manager: "StudiosManager",
) -> None:
  """
  Handles the callback query when the step to show instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - studios_manager (StudiosManager): The manager handling studio data.
  """
  query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
  text = ""
  if StudioType.Rev in query_data.studios:
    text += "*Rev Instructors:* " + ", ".join(studios_manager["Rev"].instructor_names) + "\n\n"
  if StudioType.Barrys in query_data.studios:
    text += "*Barrys Instructors:* " + ", ".join(studios_manager["Barrys"].instructor_names) + "\n\n"
  if StudioType.AbsoluteSpin in query_data.studios or StudioType.AbsolutePilates in query_data.studios:
    text += "*Absolute Instructors:* " + ", ".join(studios_manager["Absolute"].instructor_names) + "\n\n"
  if StudioType.AllySpin in query_data.studios or StudioType.AllyPilates in query_data.studios:
    text += "*Ally Instructors:* " + ", ".join(studios_manager["Ally"].instructor_names) + "\n\n"
  if StudioType.AllyRecovery in query_data.studios:
    text += "No instructors for *Ally (Recovery)\n\n"
  if StudioType.Anarchy in query_data.studios:
    text += "*Anarchy Instructors:* " + ", ".join(studios_manager["Anarchy"].instructor_names) + "\n\n"

  chat_manager.send_prompt(chat_id=query.message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
  instructors_selection_handler(message=query.message, chat_manager=chat_manager)

def rev_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter rev instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def barrys_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter barrys instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
  """
  text = "Enter instructor names separated by a comma\ne.g.: *ria*, *gino*\nEnter '*all*' to check for all instructors"
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def absolute_spin_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter absolute (spin) instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
  """
  text = "Enter instructor names separated by a comma\ne.g.: *chin*, *ria*\nEnter '*all*' to check for all instructors"
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def absolute_pilates_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter absolute (pilates) instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def ally_spin_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter ally (spin) instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def ally_pilates_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter ally (pilates) instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def anarchy_instructors_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  bot: telebot.TeleBot,
  instructorid_map: dict[str, int],
) -> None:
  """
  Handles the callback query when the step to enter anarchy instructors is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - bot (telebot.TeleBot): The instance of the Telegram bot.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
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
    instructorid_map=instructorid_map,
    chat_manager=chat_manager,
  )

def instructors_input_handler(
  message: telebot.types.Message,
  instructorid_map: dict[str, int],
  chat_manager: "ChatManager",
) -> None:
  """
  Handles user input for instructor names, validating them against the instructor map.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - instructorid_map (dict[str, int]): Dictionary of instructor names and IDs
    - chat_manager (ChatManager): The manager handling chat data.
  """
  query_data = chat_manager.get_query_data(chat_id=message.chat.id)
  updated_instructors_list = [x.strip() for x in message.text.lower().split(",")]
  if "all" in updated_instructors_list:
    query_data.studios[query_data.current_studio].instructors = ["All"]
    chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
  else:
    invalid_instructors = []
    if "/" in updated_instructors_list: # Some names contain "/" which should not be considered as a valid name
      invalid_instructors.append("/")

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
        instructor for instructor
        in updated_instructors_list
        if instructor not in invalid_instructors
      ]
      chat_manager.update_query_data_studios(chat_id=message.chat.id, studios=query_data.studios)
      text = f"Failed to find instructor(s): {', '.join(invalid_instructors)}"
      chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)

    if len(updated_instructors_list) > 0:
      query_data.studios[query_data.current_studio].instructors = updated_instructors_list

  instructors_selection_handler(message=message, chat_manager=chat_manager)

def instructors_selection_handler(message: telebot.types.Message, chat_manager: "ChatManager") -> None:
  """
  Displays the instructors selection prompt.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
  """
  query_data = chat_manager.get_query_data(chat_id=message.chat.id)
  if len(query_data.studios) == 0:
    text = "No studio selected. Please select a studio first"
    chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=None, delete_sent_msg_in_future=False)
    main_page_handler(message=message, chat_manager=chat_manager)
    return

  text = "*Currently selected instructor(s)*\n"
  text += query_data.get_query_str(include_instructors=True)

  keyboard = telebot.types.InlineKeyboardMarkup()
  if StudioType.Rev in query_data.studios:
    rev_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Rev Instructor(s)",
      callback_data="{'step': 'rev-instructors'}",
    )
    keyboard.add(rev_instructors_button)
  if StudioType.Barrys in query_data.studios:
    barrys_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Barrys Instructor(s)",
      callback_data="{'step': 'barrys-instructors'}",
    )
    keyboard.add(barrys_instructors_button)
  if StudioType.AbsoluteSpin in query_data.studios:
    absolute_spin_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Absolute (Spin) Instructor(s)",
      callback_data="{'step': 'absolute-spin-instructors'}",
    )
    keyboard.add(absolute_spin_instructors_button)
  if StudioType.AbsolutePilates in query_data.studios:
    absolute_pilates_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Absolute (Pilates) Instructor(s)",
      callback_data="{'step': 'absolute-pilates-instructors'}",
    )
    keyboard.add(absolute_pilates_instructors_button)
  if StudioType.AllySpin in query_data.studios:
    ally_spin_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Ally (Spin) Instructor(s)",
      callback_data="{'step': 'ally-spin-instructors'}",
    )
    keyboard.add(ally_spin_instructors_button)
  if StudioType.AllyPilates in query_data.studios:
    ally_pilates_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Ally (Pilates) Instructor(s)",
      callback_data="{'step': 'ally-pilates-instructors'}",
    )
    keyboard.add(ally_pilates_instructors_button)
  if StudioType.Anarchy in query_data.studios:
    anarchy_instructors_button = telebot.types.InlineKeyboardButton(
      text="Enter Anarchy Instructor(s)",
      callback_data="{'step': 'anarchy-instructors'}",
    )
    keyboard.add(anarchy_instructors_button)

  show_instructors_button = telebot.types.InlineKeyboardButton(
    text="Show Names of Instructors",
    callback_data="{'step': 'show-instructors'}",
  )
  next_button = telebot.types.InlineKeyboardButton(
    text="Next ▶️",
    callback_data="{'step': 'main-page-handler'}",
  )
  keyboard.add(show_instructors_button)
  keyboard.add(next_button)

  chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=keyboard, delete_sent_msg_in_future=True)
