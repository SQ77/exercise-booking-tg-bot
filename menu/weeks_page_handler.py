"""
weeks_page_handler.py
Author: https://github.com/lendrixxx
Description: This file defines callback queries related to selecting weeks for class schedules.
"""
import telebot
from menu.main_page_handler import main_page_handler

def weeks_selection_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the step to select week(s) is triggered.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  query_data_dict = eval(query.data)
  query_data = chat_manager.get_query_data(chat_id=query.message.chat.id)
  text = "*Currently selected week(s)*\n"
  text += query_data.get_query_str(include_weeks=True)
  text += (
    "\nAbsolute shows up to 1.5 weeks\nAlly shows up to 2 weeks\n"
    "Anarchy shows up to 2.5 weeks\nBarrys shows up to 3 weeks\nRev shows up to 4 weeks\n"
  )

  chat_manager.send_prompt(
    chat_id=query.message.chat.id,
    text=text,
    reply_markup=keyboard_manager.get_weeks_page_keyboard(),
    delete_sent_msg_in_future=True,
  )

def weeks_callback_query_handler(
  query: telebot.types.CallbackQuery,
  chat_manager: "ChatManager",
  keyboard_manager: "KeyboardManager",
) -> None:
  """
  Handles the callback query when the number of week(s) selected.

  Args:
    - query (telebot.types.CallbackQuery): The callback query object containing user interaction data.
    - chat_manager (ChatManager): The manager handling chat data.
    - keyboard_manager (KeyboardManager): The manager handling keyboard generation and interaction.
  """
  query_data_dict = eval(query.data)
  chat_manager.update_query_data_weeks(chat_id=query.message.chat.id, weeks=query_data_dict["weeks"])
  main_page_handler(message=query.message, chat_manager=chat_manager, keyboard_manager=keyboard_manager)
