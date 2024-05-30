import calendar
import requests
from bs4 import BeautifulSoup
from common.data_types import class_availability, class_data, response_availability_map, result_data, studio_location, studio_type
from copy import copy
from datetime import datetime, timedelta
from absolute.data import instructorid_map, location_map, location_str_map

def send_get_schedule_request(locations: list[studio_location], week: int, instructor: str):
    url = 'https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm?action=Reserve.chooseClass'
    params = {'wk': week}

    if 'All' in locations:
      params = {**params, **{'site': 1, 'site2': 2, 'site3': 3, 'site4': 5, 'site5': 6, 'site6': 8}}
    else:
      site_param_name = 'site'
      for location in locations:
        params[site_param_name] = location_map[location]
        if site_param_name == 'site':
          site_param_name = 'site2'
        elif site_param_name != 'site6':
          site_param_name = site_param_name[:-1] + str(int(site_param_name[-1]) + 1)
        else:
          break

    if instructor != 'All':
      params = {**params, **{'instructorid': instructorid_map[instructor]}}

    return requests.get(url=url, params=params)

def parse_get_schedule_response(response, week: int, days: list[str]) -> dict[datetime.date, list[class_data]]:
  soup = BeautifulSoup(response.text, 'html.parser')
  reserve_table_list = [table for table in soup.find_all('table') if table.get('id') == 'reserve']
  reserve_table_list_len = len(reserve_table_list)
  if reserve_table_list_len != 1:
    print(f'[W] Failed to get schedule - Expected 1 reserve table, got {reserve_table_list_len} instead')
    return {}

  reserve_table = reserve_table_list[0]
  if reserve_table.tbody is None:
    return {}

  reserve_table_rows = reserve_table.tbody.find_all('tr')
  reserve_table_rows_len = len(reserve_table_rows)
  if reserve_table_rows_len != 1:
    print(f'[W] Failed to get schedule - Expected 1 schedule row, got {reserve_table_rows_len} rows instead')
    return {}

  reserve_table_datas = reserve_table_rows[0].find_all('td')
  if len(reserve_table_datas) == 0:
    print('[W] Failed to get schedule - Table data is null')
    return {}

  # Get yesterday's date and update date at the start of each loop
  current_date = datetime.now().date() + timedelta(weeks=week) - timedelta(days=1)
  result_dict = {}
  for reserve_table_data in reserve_table_datas:
    current_date = current_date + timedelta(days=1)
    if 'All' not in days and calendar.day_name[current_date.weekday()] not in days:
      continue

    result_dict[current_date] = []
    reserve_table_data_div_list = reserve_table_data.find_all('div')
    if len(reserve_table_data_div_list) == 0:
      # Reserve table data div might be empty because schedule is only shown up to 1.5 weeks in advance
      continue

    for reserve_table_data_div in reserve_table_data_div_list:
      reserve_table_data_div_class_list = reserve_table_data_div.get('class')
      if len(reserve_table_data_div_class_list) < 2:
        availability = class_availability.Null
      else:
        availability = response_availability_map[reserve_table_data_div_class_list[1]]

      class_details = class_data(studio=studio_type.AbsoluteSpin, location=studio_location.Null, name='', instructor='', time='', availability=availability)
      for reserve_table_data_div_span in reserve_table_data_div.find_all('span'):
        reserve_table_data_div_span_class_list = reserve_table_data_div_span.get('class')
        if len(reserve_table_data_div_span_class_list) == 0:
          print('[W] Failed to get schedule - Table data span class is null')
          continue

        reserve_table_data_div_span_class = reserve_table_data_div_span_class_list[0]
        if reserve_table_data_div_span_class == 'scheduleSite':
          location_str = str(reserve_table_data_div_span.contents[0].strip())
          class_details.location = location_str_map[location_str]
        elif reserve_table_data_div_span_class == 'scheduleClass':
          class_details.name = str(reserve_table_data_div_span.contents[0].strip())
        elif reserve_table_data_div_span_class == 'scheduleInstruc':
          class_details.instructor = str(reserve_table_data_div_span.contents[0].strip())
        elif reserve_table_data_div_span_class == 'scheduleTime':
          if len(class_details.name) == 0:
            continue

          class_details.set_time(str(reserve_table_data_div_span.contents[0].strip()))
          class_details.studio = studio_type.AbsoluteSpin if 'CYCLE' in class_details.name else studio_type.AbsolutePilates
          result_dict[current_date].append(copy(class_details))

    if len(result_dict[current_date]) == 0:
      result_dict.pop(current_date)

  return result_dict

def get_absolute_schedule(locations: list[studio_location], weeks: int, days: list[str], instructors: list[str]) -> result_data:
  def _get_absolute_schedule_internal(output_result: result_data, locations: list[studio_location], weeks: int, days: list[str], instructors: list[str]) -> dict[datetime.date, list[class_data]]:
    # REST API can only select one instructor at a time
    for instructor in instructors:
      # REST API can only select one week at a time
      for week in range(0, weeks):
        get_schedule_response = send_get_schedule_request(locations=locations, instructor=instructor, week=week)
        date_class_data_list_dict = parse_get_schedule_response(get_schedule_response, week=week, days=days)
        output_result.add_classes(date_class_data_list_dict)

  result = result_data()
  # REST API can only select maximum of 5 locations at a , but there are 6 locations
  if 'All' in locations:
    location_map_list = list(location_map)
    first_location = location_map_list[0:1]
    locations = location_map_list[1:]
    _get_absolute_schedule_internal(result, first_location, weeks, days, instructors)
  elif len(locations) > 5:
    first_location = locations[0:1]
    locations = locations[1:]
    _get_absolute_schedule_internal(result, first_location, weeks, days, instructors)

  _get_absolute_schedule_internal(result, locations, weeks, days, instructors)
  return result
