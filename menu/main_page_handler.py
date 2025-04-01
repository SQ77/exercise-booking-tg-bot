"""
main_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to the main page.
"""
import telebot

def main_page_handler_callback_query_handler(query: telebot.types.CallbackQuery, chat_manager: "ChatManager") -> None:
  """
  Handles the callback query for the main page.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
  """
  main_page_handler(message=query.message, chat_manager=chat_manager)

def main_page_handler(message: telebot.types.Message, chat_manager: "ChatManager") -> None:
  """
  Handles the main page interaction, displaying the schedule and options for
  filtering by studio, instructor, week, day, time, and class name.

  Args:
    - message (telebot.types.Message): The message object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
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

  studios_button = telebot.types.InlineKeyboardButton(
    text="Studios",
    callback_data="{'step': 'studios-selection'}",
  )
  instructors_button = telebot.types.InlineKeyboardButton(
    text="Instructors",
    callback_data="{'step': 'instructors-selection'}",
  )
  weeks_button = telebot.types.InlineKeyboardButton(
    text="Weeks",
    callback_data="{'step': 'weeks-selection'}",
  )
  days_button = telebot.types.InlineKeyboardButton(
    text="Days",
    callback_data="{'step': 'days-selection'}",
  )
  time_button = telebot.types.InlineKeyboardButton(
    text="Time",
    callback_data="{'step': 'time-selection'}",
  )
  class_name_button = telebot.types.InlineKeyboardButton(
    text="Class Name",
    callback_data="{'step': 'class-name-filter-selection'}",
  )
  next_button = telebot.types.InlineKeyboardButton(
    text="Get Schedule ▶️",
    callback_data="{'step': 'get-schedule'}",
  )

  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(studios_button, instructors_button)
  keyboard.add(weeks_button, days_button)
  keyboard.add(time_button, class_name_button)
  keyboard.add(next_button)

  chat_manager.send_prompt(chat_id=message.chat.id, text=text, reply_markup=keyboard, delete_sent_msg_in_future=True)
