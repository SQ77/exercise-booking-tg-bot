import global_variables
import telebot

@global_variables.BOT.callback_query_handler(func=lambda query: eval(query.data)["step"] == "class-name-filter-selection")
def class_name_filter_selection_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  class_name_filter_selection_handler(query.from_user.id, query.message)

def class_name_filter_selection_handler(user_id: int, message: telebot.types.Message) -> None:
  query_data = global_variables.USER_MANAGER.get_query_data(user_id, message.chat.id)
  text = "*Current filter*\n"
  text += query_data.get_query_str(include_class_name_filter=True)

  keyboard = telebot.types.InlineKeyboardMarkup()
  set_filter_button = telebot.types.InlineKeyboardButton("Add Filter", callback_data="{'step': 'class-name-filter-add'}")
  reset_filter_button = telebot.types.InlineKeyboardButton("Reset Filter", callback_data="{'step': 'class-name-filter-reset'}")
  next_button = telebot.types.InlineKeyboardButton("Next ▶️", callback_data="{'step': 'main-page-handler'}")

  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(set_filter_button, reset_filter_button)
  keyboard.add(next_button)
  sent_msg = global_variables.BOT.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="Markdown")

@global_variables.BOT.callback_query_handler(func=lambda query: eval(query.data)["step"] == "class-name-filter-add")
def class_name_filter_set_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = "Enter name of class to filter (non-case sensitive)\ne.g. *essential*"
  sent_msg = global_variables.BOT.send_message(query.message.chat.id, text, parse_mode="Markdown")
  global_variables.BOT.register_next_step_handler(sent_msg, class_name_filter_input_handler, query.from_user.id)

def class_name_filter_input_handler(message: telebot.types.Message, user_id: int) -> None:
  query_data = global_variables.USER_MANAGER.get_query_data(user_id, message.chat.id)
  query_data.class_name_filter = message.text
  class_name_filter_selection_handler(user_id, message)

@global_variables.BOT.callback_query_handler(func=lambda query: eval(query.data)["step"] == "class-name-filter-reset")
def class_name_filter_reset_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data = global_variables.USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  query_data.class_name_filter = ""
  class_name_filter_selection_handler(query.from_user.id, query.message)
