import absolute
import ally
import barrys
import os
import rev
import telebot
import time
import threading
import schedule
from absolute.absolute import get_absolute_schedule
from absolute.data import PILATES_INSTRUCTOR_NAMES as ABSOLUTE_PILATES_INSTRUCTOR_NAMES
from absolute.data import SPIN_INSTRUCTOR_NAMES as ABSOLUTE_SPIN_INSTRUCTOR_NAMES
from ally.ally import get_ally_schedule
from ally.data import PILATES_INSTRUCTOR_NAMES as ALLY_PILATES_INSTRUCTOR_NAMES
from ally.data import SPIN_INSTRUCTOR_NAMES as ALLY_SPIN_INSTRUCTOR_NAMES
from barrys.barrys import get_barrys_schedule
from barrys.data import INSTRUCTOR_NAMES as BARRYS_INSTRUCTOR_NAMES
from common.data_types import QueryData, ResultData, SORTED_DAYS, StudioData, StudioLocation, STUDIO_LOCATIONS_MAP, StudioType
from copy import copy
from rev.data import INSTRUCTOR_NAMES as REV_INSTRUCTOR_NAMES
from rev.rev import get_rev_schedule
from user_manager import UserManager

# Global variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT = telebot.TeleBot(BOT_TOKEN)
START_COMMAND = telebot.types.BotCommand(command='start', description='Check schedules')
NERD_COMMAND = telebot.types.BotCommand(command='nerd', description='Nerd mode')
INSTRUCTORS_COMMAND = telebot.types.BotCommand(command='instructors', description='Show list of instructors')
BOT.set_my_commands([START_COMMAND, NERD_COMMAND, INSTRUCTORS_COMMAND])

USER_MANAGER = UserManager()
CACHED_RESULT_DATA = ResultData()

def get_locations_keyboard(user_id: int, chat_id: int) -> telebot.types.InlineKeyboardMarkup:
  query_data = USER_MANAGER.get_query_data(user_id, chat_id)
  button_data = USER_MANAGER.get_button_data(user_id, chat_id)
  locations_keyboard = telebot.types.InlineKeyboardMarkup()
  if query_data.current_studio == 'Rev':
    locations_keyboard.add(button_data.studios_locations_buttons_map['Rev']['Bugis'], button_data.studios_locations_buttons_map['Rev']['Orchard'])
    locations_keyboard.add(button_data.studios_locations_buttons_map['Rev']['Suntec'], button_data.studios_locations_buttons_map['Rev']['TJPG'])
  elif query_data.current_studio == 'Barrys':
    locations_keyboard.add(button_data.studios_locations_buttons_map['Barrys']['Orchard'], button_data.studios_locations_buttons_map['Barrys']['Raffles'])
  elif query_data.current_studio == 'Absolute (Spin)':
    locations_keyboard.add(button_data.studios_locations_buttons_map['Absolute (Spin)']['Centrepoint'], button_data.studios_locations_buttons_map['Absolute (Spin)']['i12'])
    locations_keyboard.add(button_data.studios_locations_buttons_map['Absolute (Spin)']['Star Vista'], button_data.studios_locations_buttons_map['Absolute (Spin)']['Raffles'])
    locations_keyboard.add(button_data.studios_locations_buttons_map['Absolute (Spin)']['Millenia Walk'])
  elif query_data.current_studio == 'Absolute (Pilates)':
    locations_keyboard.add(button_data.studios_locations_buttons_map['Absolute (Pilates)']['Centrepoint'], button_data.studios_locations_buttons_map['Absolute (Pilates)']['i12'])
    locations_keyboard.add(button_data.studios_locations_buttons_map['Absolute (Pilates)']['Star Vista'], button_data.studios_locations_buttons_map['Absolute (Pilates)']['Raffles'])
    locations_keyboard.add(button_data.studios_locations_buttons_map['Absolute (Pilates)']['Great World'])
  elif query_data.current_studio == 'Ally (Spin)':
    locations_keyboard.add(button_data.studios_locations_buttons_map['Ally (Spin)']['Cross Street'])
  elif query_data.current_studio == 'Ally (Pilates)':
    locations_keyboard.add(button_data.studios_locations_buttons_map['Ally (Pilates)']['Cross Street'])
  locations_keyboard.add(button_data.locations_select_all_button, button_data.locations_unselect_all_button)
  locations_keyboard.add(button_data.locations_select_more_studios_button, button_data.locations_next_button)
  return locations_keyboard

def get_days_keyboard(user_id: int, chat_id: int) -> telebot.types.InlineKeyboardMarkup:
  button_data = USER_MANAGER.get_button_data(user_id, chat_id)
  days_keyboard = telebot.types.InlineKeyboardMarkup()
  days_keyboard.add(button_data.days_buttons_map['Monday'], button_data.days_buttons_map['Tuesday'])
  days_keyboard.add(button_data.days_buttons_map['Wednesday'], button_data.days_buttons_map['Thursday'])
  days_keyboard.add(button_data.days_buttons_map['Friday'], button_data.days_buttons_map['Saturday'])
  days_keyboard.add(button_data.days_buttons_map['Sunday'])
  days_keyboard.add(button_data.days_select_all_button, button_data.days_unselect_all_button)
  days_keyboard.add(button_data.days_back_button, button_data.days_next_button)
  return days_keyboard

def send_results(query: telebot.types.CallbackQuery) -> None:
  global CACHED_RESULT_DATA
  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  result = CACHED_RESULT_DATA.get_data(query_data)
  USER_MANAGER.reset_query_data(query.from_user.id, query.message.chat.id)

  # Send string as messages
  schedule_str = result.get_result_str()
  if len(schedule_str) > 4095:
    shortened_message = ''
    for line in schedule_str.splitlines():
      is_new_day = any(day in line for day in SORTED_DAYS) and len(shortened_message) > 0
      max_len_reached = len(shortened_message) + len(line) > 4095
      if is_new_day or max_len_reached:
        BOT.send_message(query.message.chat.id, shortened_message, parse_mode='Markdown')
        shortened_message = line + '\n'
      else:
        shortened_message += line + '\n'

    if len(shortened_message) > 0:
      BOT.send_message(query.message.chat.id, shortened_message, parse_mode='Markdown')
  else:
    BOT.send_message(query.message.chat.id, schedule_str, parse_mode='Markdown')

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'studios')
def studios_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data_dict = eval(query.data)
  studio_selected = query_data_dict['studios']
  if studio_selected == 'All':
    USER_MANAGER.update_query_data_select_all_studios(query.from_user.id, query.message.chat.id)
    USER_MANAGER.update_button_data_select_all_studios_locations_buttons_map(query.from_user.id, query.message.chat.id)
    studios_handler(query.from_user.id, query.message)
  elif studio_selected == 'None':
    USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, {})
    USER_MANAGER.reset_button_data_studios_locations_buttons_map(query.from_user.id, query.message.chat.id)
    studios_handler(query.from_user.id, query.message)
  else:
    USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, studio_selected)
    locations_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'locations')
def locations_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  button_data = USER_MANAGER.get_button_data(query.from_user.id, query.message.chat.id)
  query_data_dict = eval(query.data)
  selected_studio_location = StudioLocation[query_data_dict['locations']]
  if selected_studio_location == StudioLocation.Null:
    for location in button_data.studios_locations_buttons_map[query_data.current_studio]:
      button_data.studios_locations_buttons_map[query_data.current_studio][location] = telebot.types.InlineKeyboardButton(location, callback_data=button_data.studios_locations_buttons_map[query_data.current_studio][location].callback_data)
    USER_MANAGER.update_button_data_studios_locations_buttons_map(query.from_user.id, query.message.chat.id, button_data.studios_locations_buttons_map)
    query_data.studios.pop(query_data.current_studio)
    USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, query_data.studios)
  elif selected_studio_location == StudioLocation.All:
    for location in button_data.studios_locations_buttons_map[query_data.current_studio]:
      button_data.studios_locations_buttons_map[query_data.current_studio][location] = telebot.types.InlineKeyboardButton(location + ' ✅', callback_data=button_data.studios_locations_buttons_map[query_data.current_studio][location].callback_data)
    USER_MANAGER.update_button_data_studios_locations_buttons_map(query.from_user.id, query.message.chat.id, button_data.studios_locations_buttons_map)
    if query_data.current_studio not in query_data.studios:
      new_studio = {query_data.current_studio: StudioData(locations=copy(STUDIO_LOCATIONS_MAP[query_data.current_studio]))}
      query_data.studios = {**query_data.studios, **new_studio}
      USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, query_data.studios)
    else:
      query_data.studios[query_data.current_studio].locations = copy(STUDIO_LOCATIONS_MAP[query_data.current_studio])
      USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, query_data.studios)
  else:
    if query_data.current_studio not in query_data.studios:
      button_data.studios_locations_buttons_map[query_data.current_studio][selected_studio_location] = \
        telebot.types.InlineKeyboardButton(
          selected_studio_location + ' ✅',
          callback_data=button_data.studios_locations_buttons_map[query_data.current_studio][selected_studio_location].callback_data)
      USER_MANAGER.update_button_data_studios_locations_buttons_map(query.from_user.id, query.message.chat.id, button_data.studios_locations_buttons_map)
      new_studio = {query_data.current_studio: StudioData(locations=[selected_studio_location])}
      query_data.studios = {**query_data.studios, **new_studio}
      USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, query_data.studios)
    elif selected_studio_location in query_data.studios[query_data.current_studio].locations:
      button_data.studios_locations_buttons_map[query_data.current_studio][selected_studio_location] = \
        telebot.types.InlineKeyboardButton(
          selected_studio_location,
          callback_data=button_data.studios_locations_buttons_map[query_data.current_studio][selected_studio_location].callback_data)
      USER_MANAGER.update_button_data_studios_locations_buttons_map(query.from_user.id, query.message.chat.id, button_data.studios_locations_buttons_map)
      query_data.studios[query_data.current_studio].locations.remove(selected_studio_location)
      if len(query_data.studios[query_data.current_studio].locations) == 0:
        query_data.studios.pop(query_data.current_studio)
      USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, query_data.studios)
    else:
      button_data.studios_locations_buttons_map[query_data.current_studio][selected_studio_location] = telebot.types.InlineKeyboardButton(selected_studio_location + ' ✅', callback_data=button_data.studios_locations_buttons_map[query_data.current_studio][selected_studio_location].callback_data)
      USER_MANAGER.update_button_data_studios_locations_buttons_map(query.from_user.id, query.message.chat.id, button_data.studios_locations_buttons_map)
      query_data.studios[query_data.current_studio].locations.append(selected_studio_location)
      USER_MANAGER.update_query_data_studios(query.from_user.id, query.message.chat.id, query_data.studios)

  text = query_data.get_query_str(include_studio=True)
  text += '*Select the location(s) to check*'

  BOT.edit_message_text(
    chat_id=button_data.locations_selection_message.chat.id,
    message_id=button_data.locations_selection_message.id,
    text=text,
    reply_markup=get_locations_keyboard(query.from_user.id, query.message.chat.id),
    parse_mode='Markdown')

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'locations-select-more-studios')
def locations_back_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  studios_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'studios-next')
def studios_next_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  if len(query_data.studios) == 0:
    text = 'Please select a studio'
    sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
    studios_handler(query.from_user.id, query.message)
  else:
    instructors_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'weeks')
def weeks_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data_dict = eval(query.data)
  USER_MANAGER.update_query_data_weeks(query.from_user.id, query.message.chat.id, query_data_dict['weeks'])
  days_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'weeks-back')
def weeks_back_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  instructors_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'days')
def days_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  button_data = USER_MANAGER.get_button_data(query.from_user.id, query.message.chat.id)
  query_data_dict = eval(query.data)
  selected_day = query_data_dict['days']
  if selected_day == 'None':
    for day in button_data.days_buttons_map:
      button_data.days_buttons_map[day] = telebot.types.InlineKeyboardButton(day, callback_data=button_data.days_buttons_map[day].callback_data)
    USER_MANAGER.update_button_data_days_buttons_map(query.from_user.id, query.message.chat.id, button_data.days_buttons_map)
    USER_MANAGER.update_query_data_days(query.from_user.id, query.message.chat.id, [])
  elif selected_day == 'All':
    for day in button_data.days_buttons_map:
      button_data.days_buttons_map[day] = telebot.types.InlineKeyboardButton(day + ' ✅', callback_data=button_data.days_buttons_map[day].callback_data)
    USER_MANAGER.update_button_data_days_buttons_map(query.from_user.id, query.message.chat.id, button_data.days_buttons_map)
    USER_MANAGER.update_query_data_days(query.from_user.id, query.message.chat.id, SORTED_DAYS)
  else:
    query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
    if selected_day in query_data.days:
      button_data.days_buttons_map[selected_day] = telebot.types.InlineKeyboardButton(selected_day, callback_data=button_data.days_buttons_map[selected_day].callback_data)
      USER_MANAGER.update_button_data_days_buttons_map(query.from_user.id, query.message.chat.id, button_data.days_buttons_map)
      query_data.days.remove(selected_day)
      USER_MANAGER.update_query_data_days(query.from_user.id, query.message.chat.id, query_data.days)
    else:
      button_data.days_buttons_map[selected_day] = telebot.types.InlineKeyboardButton(selected_day + ' ✅', callback_data=button_data.days_buttons_map[selected_day].callback_data)
      USER_MANAGER.update_button_data_days_buttons_map(query.from_user.id, query.message.chat.id, button_data.days_buttons_map)
      query_data.days.append(selected_day)
      query_data.days = sorted(query_data.days, key=SORTED_DAYS.index)
      USER_MANAGER.update_query_data_days(query.from_user.id, query.message.chat.id, query_data.days)

  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  text = query_data.get_query_str(include_studio=True, include_instructors=True, include_weeks=True, include_days=True)
  text += '*Select the day(s) to show classes of*'

  button_data = USER_MANAGER.get_button_data(query.from_user.id, query.message.chat.id)
  BOT.edit_message_text(
    chat_id=button_data.days_selection_message.chat.id,
    message_id=button_data.days_selection_message.id,
    text=text,
    reply_markup=get_days_keyboard(query.from_user.id, query.message.chat.id),
    parse_mode='Markdown')

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'days-back')
def days_back_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  weeks_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'days-next')
def days_next_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  if len(query_data.days) == 0:
    text = 'Please select a day'
    sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
    days_handler(query.from_user.id, query.message)
    return

  send_results(query)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'rev-instructors')
def rev_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = 'Enter instructor names separated by a comma\ne.g.: *chloe*, *jerlyn*, *zai*\nEnter "*all*" to check for all instructors'
  USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, 'Rev')
  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, instructors_input_handler, query.from_user.id, rev.data.INSTRUCTORID_MAP)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'barrys-instructors')
def barrys_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = 'Enter instructor names separated by a comma\ne.g.: *ria*, *gino*\nEnter "*all*" to check for all instructors'
  USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, 'Barrys')
  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, instructors_input_handler, query.from_user.id, barrys.data.INSTRUCTORID_MAP)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'absolute-spin-instructors')
def absolute_spin_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = 'Enter instructor names separated by a comma\ne.g.: *chin*, *ria*\nEnter "*all*" to check for all instructors'
  USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, 'Absolute (Spin)')
  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, instructors_input_handler, query.from_user.id, absolute.data.SPIN_INSTRUCTORID_MAP)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'absolute-pilates-instructors')
def absolute_pilates_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = 'Enter instructor names separated by a comma\ne.g.: *daniella*, *vnex*\nEnter "*all*" to check for all instructors'
  USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, 'Absolute (Pilates)')
  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, instructors_input_handler, query.from_user.id, absolute.data.PILATES_INSTRUCTORID_MAP)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'ally-spin-instructors')
def ally_spin_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = 'Enter instructor names separated by a comma\ne.g.: *samuel*, *jasper*\nEnter "*all*" to check for all instructors'
  USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, 'Ally (Spin)')
  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, instructors_input_handler, query.from_user.id, ally.data.SPIN_INSTRUCTORID_MAP)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'ally-pilates-instructors')
def ally_pilates_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  text = 'Enter instructor names separated by a comma\ne.g.: *candice*, *ruth*\nEnter "*all*" to check for all instructors'
  USER_MANAGER.update_query_data_current_studio(query.from_user.id, query.message.chat.id, 'Ally (Pilates)')
  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, instructors_input_handler, query.from_user.id, ally.data.PILATES_INSTRUCTORID_MAP)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'show-instructors')
def show_instructors_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  text = ''
  if 'Rev' in query_data.studios:
    text += '*Rev Instructors:* ' + ', '.join(rev.data.INSTRUCTOR_NAMES) + '\n\n'
  if 'Barrys' in query_data.studios:
    text += '*Barrys Instructors:* ' + ', '.join(barrys.data.INSTRUCTOR_NAMES) + '\n\n'
  if 'Absolute (Spin)' in query_data.studios:
    text += '*Absolute (Spin) Instructors:* ' + ', '.join(absolute.data.SPIN_INSTRUCTOR_NAMES) + '\n\n'
  if 'Absolute (Pilates)' in query_data.studios:
    text += '*Absolute (Pilates) Instructors:* ' + ', '.join(absolute.data.PILATES_INSTRUCTOR_NAMES) + '\n\n'
  if 'Ally (Spin)' in query_data.studios:
    text += '*Ally (Spin) Instructors:* ' + ', '.join(ally.data.SPIN_INSTRUCTOR_NAMES) + '\n\n'
  if 'Ally (Pilates)' in query_data.studios:
    text += '*Ally (Pilates) Instructors:* ' + ', '.join(ally.data.PILATES_INSTRUCTOR_NAMES) + '\n\n'

  sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
  instructors_handler(query.from_user.id, query.message)

def instructors_input_handler(message: telebot.types.Message, user_id: int, instructorid_map: dict[str, int]) -> None:
  query_data = USER_MANAGER.get_query_data(user_id, message.chat.id)
  query_data.studios[query_data.current_studio].instructors = [x.strip() for x in message.text.lower().split(',')]
  if 'all' in query_data.studios[query_data.current_studio].instructors:
    query_data.studios[query_data.current_studio].instructors = ['All']
    USER_MANAGER.update_query_data_studios(user_id, message.chat.id, query_data.studios)
  else:
    invalid_instructors = []
    for instructor in query_data.studios[query_data.current_studio].instructors:
      instructor_in_map = (any(instructor in instructor_in_map.split(' ') for instructor_in_map in instructorid_map)
        or any(instructor == instructor_in_map for instructor_in_map in instructorid_map))
      if not instructor_in_map:
        invalid_instructors.append(instructor)

    if len(invalid_instructors) > 0:
      query_data.studios[query_data.current_studio].instructors = [
        instructor for instructor
        in query_data.studios[query_data.current_studio].instructors
        if instructor not in invalid_instructors
      ]
      USER_MANAGER.update_query_data_studios(user_id, message.chat.id, query_data.studios)
      text = f'Failed to find instructor(s): {", ".join(invalid_instructors)}'
      sent_msg = BOT.send_message(message.chat.id, text, parse_mode='Markdown')

  instructors_handler(user_id, message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'instructors-next')
def instructors_next_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  global CACHED_RESULT_DATA
  query_data = USER_MANAGER.get_query_data(query.from_user.id, query.message.chat.id)
  if not query_data.has_instructors_selected():
    text = 'Please select at least one instructor'
    sent_msg = BOT.send_message(query.message.chat.id, text, parse_mode='Markdown')
    instructors_handler(query.from_user.id, query.message)
  else:
    weeks_handler(query.from_user.id, query.message)

@BOT.callback_query_handler(func=lambda query: eval(query.data)['step'] == 'instructors-back')
def instructors_back_callback_query_handler(query: telebot.types.CallbackQuery) -> None:
  studios_handler(query.from_user.id, query.message)

@BOT.message_handler(commands=['start'])
def start_handler(message: telebot.types.Message) -> None:
  USER_MANAGER.reset_query_data(message.from_user.id, message.chat.id)
  USER_MANAGER.reset_button_data(message.from_user.id, message.chat.id)
  studios_handler(message.from_user.id, message)

def studios_handler(user_id: int, message: telebot.types.Message) -> None:
  query_data = USER_MANAGER.get_query_data(user_id, message.chat.id)
  text = query_data.get_query_str(include_studio=True)
  text += '*Select the studio(s) to check*'

  rev_button = telebot.types.InlineKeyboardButton('Rev', callback_data='{"studios": "Rev", "step": "studios"}')
  barrys_button = telebot.types.InlineKeyboardButton('Barrys', callback_data='{"studios": "Barrys", "step": "studios"}')
  absolute_spin_button = telebot.types.InlineKeyboardButton('Absolute (Spin)', callback_data='{"studios": "Absolute (Spin)", "step": "studios"}')
  absolute_pilates_button = telebot.types.InlineKeyboardButton('Absolute (Pilates)', callback_data='{"studios": "Absolute (Pilates)", "step": "studios"}')
  ally_spin_button = telebot.types.InlineKeyboardButton('Ally (Spin)', callback_data='{"studios": "Ally (Spin)", "step": "studios"}')
  ally_pilates_button = telebot.types.InlineKeyboardButton('Ally (Pilates)', callback_data='{"studios": "Ally (Pilates)", "step": "studios"}')
  select_all_button = telebot.types.InlineKeyboardButton('Select All', callback_data='{"studios": "All", "step": "studios"}')
  unselect_all_button = telebot.types.InlineKeyboardButton('Unselect All', callback_data='{"studios": "None", "step": "studios"}')
  next_button = telebot.types.InlineKeyboardButton('Next ▶️', callback_data='{"step": "studios-next"}')

  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(rev_button, barrys_button)
  keyboard.add(absolute_spin_button, absolute_pilates_button)
  keyboard.add(ally_spin_button, ally_pilates_button)
  keyboard.add(select_all_button, unselect_all_button)
  keyboard.add(next_button)
  sent_msg = BOT.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')


@BOT.message_handler(commands=['instructors'])
def instructors_list_handler(message: telebot.types.Message) -> None:
  text = '*Rev Instructors:* ' + ', '.join(rev.data.INSTRUCTOR_NAMES) + '\n\n'
  text += '*Barrys Instructors:* ' + ', '.join(barrys.data.INSTRUCTOR_NAMES) + '\n\n'
  text += '*Absolute (Spin) Instructors:* ' + ', '.join(absolute.data.SPIN_INSTRUCTOR_NAMES) + '\n\n'
  text += '*Absolute (Pilates) Instructors:* ' + ', '.join(absolute.data.PILATES_INSTRUCTOR_NAMES) + '\n\n'
  text += '*Ally (Spin) Instructors:* ' + ', '.join(ally.data.SPIN_INSTRUCTOR_NAMES) + '\n\n'
  text += '*Ally (Pilates) Instructors:* ' + ', '.join(ally.data.PILATES_INSTRUCTOR_NAMES) + '\n\n'
  sent_msg = BOT.send_message(message.chat.id, text, parse_mode='Markdown')

@BOT.message_handler(commands=['nerd'])
def nerd_handler(message: telebot.types.Message) -> None:
  text = "Welcome to nerd mode 🤓\n" \
         "\n" \
         "*Enter your query in the following format:*\n" \
         "Studio name\n" \
         "Studio locations (comma separated)\n" \
         "Instructor names (comma separated)\n" \
         "(Repeat above for multiple studios)\n" \
         "Weeks\n" \
         "Days\n" \
         "\n" \
         "*Studio names*: rev, barrys, absolute (spin), absolute (pilates), ally (spin), ally (pilates)\n" \
         "*Studio locations*: orchard, tjpg, bugis, suntec, raffles, centrepoint, i12, millenia walk, star vista, great world\n" \
         "*Instructors*: Use /instructors for list of instructors\n" \
         "\n" \
         "*e.g.*\n" \
         "rev\n" \
         "bugis, orchard\n" \
         "chloe, zai\n" \
         "absolute (spin)\n" \
         "raffles\n" \
         "ria\n" \
         "2\n" \
         "monday, wednesday, saturday\n"

  sent_msg = BOT.send_message(message.chat.id, text, parse_mode='Markdown')
  BOT.register_next_step_handler(sent_msg, nerd_input_handler)

def nerd_input_handler(message: telebot.types.Message) -> None:
  '''
  Expected message format:
  /nerd
  Studio name
  Comma separated studio locations
  Comma separated instructor names
  Studio name (If selecting multiple studios)
  Comma separated studio locations (If selecting multiple studios)
  Comma separated instructor names (If selecting multiple studios)
  Weeks
  Days

  e.g.
  /nerd
  rev
  bugis, orchard
  chloe, zai
  absolute (spin)
  raffles
  ria
  2
  monday, wednesday, saturday
  '''
  input_str_list = message.text.splitlines()

  # Weeks and days = 2 items. Remaining items should be divisible by 3 (studio name, locations, instructors)
  if (len(input_str_list) - 2) % 3 != 0:
    BOT.send_message(message.chat.id, 'Failed to handle query. Unexpected format received.', parse_mode='Markdown')
    return

  # Loop through studios
  query = QueryData(studios={}, current_studio=StudioType.Null, weeks=0, days=[])
  current_studio = StudioType.Null
  current_studio_locations = []
  for index, input_str in enumerate(input_str_list[:-2]):
    step = index % 3
    if step == 0: # Studio name
      selected_studio = None
      found_studio = False
      for studio in StudioType:
        if input_str.lower() == studio.value.lower():
          current_studio = studio
          found_studio = True
          break
      if not found_studio:
        BOT.send_message(message.chat.id, f'Failed to handle query. Unexpected studio name \'{input_str}\'', parse_mode='Markdown')
        return
    elif step == 1: # Studio locations
      selected_locations = [x.strip() for x in input_str.split(',')]
      for selected_location in selected_locations:
        found_location = False
        for location in StudioLocation:
          if selected_location.lower() == location.value.lower():
            current_studio_locations.append(location)
            found_location = True
            break
        if not found_location:
          BOT.send_message(message.chat.id, f'Failed to handle query. Unexpected studio name \'{selected_location}\'', parse_mode='Markdown')
          return
    elif step == 2: # Studio instructors
      instructor_list = []
      if current_studio == StudioType.Rev:
        instructor_list = REV_INSTRUCTOR_NAMES
      elif current_studio == StudioType.Barrys:
        instructor_list = BARRYS_INSTRUCTOR_NAMES
      elif current_studio == StudioType.AbsolutePilates:
        instructor_list = ABSOLUTE_PILATES_INSTRUCTOR_NAMES
      elif current_studio == StudioType.AbsoluteSpin:
        instructor_list = ABSOLUTE_SPIN_INSTRUCTOR_NAMES
      elif current_studio == StudioType.AllyPilates:
        instructor_list = ALLY_PILATES_INSTRUCTOR_NAMES
      elif current_studio == StudioType.AllySpin:
        instructor_list = ALLY_SPIN_INSTRUCTOR_NAMES

      selected_instructors = [x.strip().lower() for x in input_str.split(',')]
      invalid_instructors = []
      if 'all' in selected_instructors:
        selected_instructors = ['All']
      else:
        for instructor in selected_instructors:
          found_instructor = (any(instructor in instructor_in_list.split(' ') for instructor_in_list in instructor_list)
            or any(instructor == instructor_in_list for instructor_in_list in instructor_list))
          if not found_instructor:
            invalid_instructors.append(instructor)

      if len(invalid_instructors) > 0:
        selected_instructors = [instructor for instructor in selected_instructors if instructor not in invalid_instructors]
        text = f'Failed to find instructor(s): {", ".join(invalid_instructors)}'
        sent_msg = BOT.send_message(message.chat.id, text, parse_mode='Markdown')

      if len(selected_instructors) == 0:
        BOT.send_message(message.chat.id, f'Failed to handle query. No instructor selected for {current_studio}', parse_mode='Markdown')
        return

      query.studios[current_studio] = StudioData(locations=current_studio_locations, instructors = selected_instructors)

  # Get number of weeks
  try:
    query.weeks = int(input_str_list[-2])
  except:
    BOT.send_message(message.chat.id, f'Failed to handle query. Invalid input for \'weeks\'. Expected number, got {input_str_list[-2]}', parse_mode='Markdown')
    return

  # Get list of days
  query.days = [x.strip().capitalize() for x in input_str_list[-1].split(',')]
  if 'All' in query.days:
    query.days = ['All']
  else:
    for selected_day in query.days:
      if selected_day.capitalize() not in SORTED_DAYS:
        BOT.send_message(message.chat.id, f'Failed to handle query. Invalid input for \'days\'. Unknown day {selected_day}', parse_mode='Markdown')
        return

  result = CACHED_RESULT_DATA.get_data(query)

  # Send string as messages
  schedule_str = result.get_result_str()
  if len(schedule_str) > 4095:
    shortened_message = ''
    for line in schedule_str.splitlines():
      is_new_day = any(day in line for day in SORTED_DAYS) and len(shortened_message) > 0
      max_len_reached = len(shortened_message) + len(line) > 4095
      if is_new_day or max_len_reached:
        BOT.send_message(message.chat.id, shortened_message, parse_mode='Markdown')
        shortened_message = line + '\n'
      else:
        shortened_message += line + '\n'

    if len(shortened_message) > 0:
      BOT.send_message(message.chat.id, shortened_message, parse_mode='Markdown')
  else:
    BOT.send_message(message.chat.id, schedule_str, parse_mode='Markdown')


@BOT.message_handler(commands=['refresh'])
def refresh_handler(message: telebot.types.Message) -> None:
  text = 'Updating cached schedules...'
  sent_msg = BOT.send_message(message.chat.id, text, parse_mode='Markdown')
  update_cached_result_data()
  text = 'Finished updating schedules'
  sent_msg = BOT.send_message(message.chat.id, text, parse_mode='Markdown')

def locations_handler(user_id: int, message: telebot.types.Message):
  query_data = USER_MANAGER.get_query_data(user_id, message.chat.id)
  text = query_data.get_query_str(include_studio=True)
  text += '*Select the location(s) to check*'

  sent_msg = BOT.send_message(
    message.chat.id, text, reply_markup=get_locations_keyboard(user_id, message.chat.id), parse_mode='Markdown')
  USER_MANAGER.update_button_data_locations_selection_message(user_id, message.chat.id, sent_msg)

def weeks_handler(user_id: int, message: telebot.types.Message) -> None:
  query_data = USER_MANAGER.get_query_data(user_id, message.chat.id)
  text = query_data.get_query_str(include_studio=True, include_instructors=True, include_weeks=True)
  text += '*Select the number of weeks of classes to show*\n'
  text += 'Absolute shows up to 1.5 weeks\nAlly shows up to 2 weeks\nBarrys shows up to 3 weeks\nRev shows up to 4 weeks\n'

  one_button = telebot.types.InlineKeyboardButton('1', callback_data='{"weeks": 1, "step": "weeks"}')
  two_button = telebot.types.InlineKeyboardButton('2', callback_data='{"weeks": 2, "step": "weeks"}')
  three_button = telebot.types.InlineKeyboardButton('3', callback_data='{"weeks": 3, "step": "weeks"}')
  four_button = telebot.types.InlineKeyboardButton('4', callback_data='{"weeks": 4, "step": "weeks"}')
  back_button = telebot.types.InlineKeyboardButton('◀️ Back', callback_data='{"step": "weeks-back"}')

  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.add(one_button, two_button)
  keyboard.add(three_button, four_button)
  keyboard.add(back_button)
  sent_msg = BOT.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')

def days_handler(user_id: int, message: telebot.types.Message) -> None:
  query_data = USER_MANAGER.get_query_data(user_id, message.chat.id)
  text = query_data.get_query_str(include_studio=True, include_instructors=True, include_weeks=True, include_days=True)
  text += '*Select the day(s) to show classes of*'
  USER_MANAGER.reset_button_data_days_buttons_map(user_id, message.chat.id)

  sent_msg = BOT.send_message(message.chat.id, text, reply_markup=get_days_keyboard(user_id, message.chat.id), parse_mode='Markdown')
  USER_MANAGER.update_button_data_days_selection_message(user_id, message.chat.id, sent_msg)

def instructors_handler(user_id: int, message: telebot.types.Message) -> None:
  query_data = USER_MANAGER.get_query_data(user_id, message.chat.id)
  text = query_data.get_query_str(include_studio=True, include_instructors=True)
  text += '*Select the studio to choose instructors*'

  keyboard = telebot.types.InlineKeyboardMarkup()
  if 'Rev' in query_data.studios:
    rev_instructors_button = telebot.types.InlineKeyboardButton('Enter Rev Instructor(s)', callback_data='{"step": "rev-instructors"}')
    keyboard.add(rev_instructors_button)
  if 'Barrys' in query_data.studios:
    barrys_instructors_button = telebot.types.InlineKeyboardButton('Enter Barrys Instructor(s)', callback_data='{"step": "barrys-instructors"}')
    keyboard.add(barrys_instructors_button)
  if 'Absolute (Spin)' in query_data.studios:
    absolute_spin_instructors_button = telebot.types.InlineKeyboardButton('Enter Absolute (Spin) Instructor(s)', callback_data='{"step": "absolute-spin-instructors"}')
    keyboard.add(absolute_spin_instructors_button)
  if 'Absolute (Pilates)' in query_data.studios:
    absolute_pilates_instructors_button = telebot.types.InlineKeyboardButton('Enter Absolute (Pilates) Instructor(s)', callback_data='{"step": "absolute-pilates-instructors"}')
    keyboard.add(absolute_pilates_instructors_button)
  if 'Ally (Spin)' in query_data.studios:
    ally_spin_instructors_button = telebot.types.InlineKeyboardButton('Enter Ally (Spin) Instructor(s)', callback_data='{"step": "ally-spin-instructors"}')
    keyboard.add(ally_spin_instructors_button)
  if 'Ally (Pilates)' in query_data.studios:
    ally_pilates_instructors_button = telebot.types.InlineKeyboardButton('Enter Ally (Pilates) Instructor(s)', callback_data='{"step": "ally-pilates-instructors"}')
    keyboard.add(ally_pilates_instructors_button)

  show_instructors_button = telebot.types.InlineKeyboardButton('Show Names of Instructors', callback_data='{"step": "show-instructors"}')
  next_button = telebot.types.InlineKeyboardButton('Next ▶️', callback_data='{"step": "instructors-next"}')
  back_button = telebot.types.InlineKeyboardButton('◀️ Back', callback_data='{"step": "instructors-back"}')
  keyboard.add(show_instructors_button)
  keyboard.add(back_button, next_button)
  sent_msg = BOT.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')

def update_cached_result_data() -> None:
  global CACHED_RESULT_DATA
  print('Updating cached result data...')
  CACHED_RESULT_DATA = get_absolute_schedule(locations=[StudioLocation.All], weeks=2, days=['All'], instructors=['All'])
  CACHED_RESULT_DATA += get_ally_schedule(weeks=2, days=['All'], instructors=['All'])
  CACHED_RESULT_DATA += get_barrys_schedule(locations=[StudioLocation.All], weeks=3, days=['All'], instructors=['All'])
  CACHED_RESULT_DATA += get_rev_schedule(locations=[StudioLocation.All], weeks=4, days=['All'], instructors=['All'])
  print('Successfully updated cached result data!')

def schedule_update_cached_result_data(stop_event) -> None:
  schedule.every().day.at("00:00").do(update_cached_result_data)
  while not stop_event.is_set():
    schedule.run_pending()
    time.sleep(1)

if __name__ =="__main__":
  stop_event = threading.Event()
  update_schedule_thread = threading.Thread(target=schedule_update_cached_result_data, args=[stop_event])
  update_schedule_thread.start()

  print('Starting bot...')
  update_cached_result_data()
  print('Bot started!')

  BOT.infinity_polling()

  stop_event.set()
  update_schedule_thread.join()