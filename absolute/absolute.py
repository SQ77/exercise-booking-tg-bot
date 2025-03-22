import calendar
import global_variables
import requests
from bs4 import BeautifulSoup
from common.data_types import CapacityInfo, ClassAvailability, ClassData, RESPONSE_AVAILABILITY_MAP, ResultData, StudioLocation, StudioType
from copy import copy
from datetime import datetime, timedelta
from absolute.data import LOCATION_MAP, LOCATION_STR_MAP

def send_get_schedule_request(locations: list[StudioLocation], week: int) -> requests.models.Response:
  url = 'https://absoluteboutiquefitness.zingfit.com/reserve/index.cfm?action=Reserve.chooseClass'
  params = {'wk': week}

  if 'All' in locations:
    params = {**params, **{'site': 1, 'site2': 2, 'site3': 3, 'site4': 5, 'site5': 6, 'site6': 8}}
  else:
    site_param_name = 'site'
    for location in locations:
      params[site_param_name] = LOCATION_MAP[location]
      if site_param_name == 'site':
        site_param_name = 'site2'
      elif site_param_name != 'site6':
        site_param_name = site_param_name[:-1] + str(int(site_param_name[-1]) + 1)
      else:
        break

  return requests.get(url=url, params=params)

def parse_get_schedule_response(response: requests.models.Response, locations: list[StudioLocation], week: int) -> dict[datetime.date, list[ClassData]]:
  soup = BeautifulSoup(response.text, 'html.parser')
  reserve_table_list = [table for table in soup.find_all('table') if table.get('id') == 'reserve']
  reserve_table_list_len = len(reserve_table_list)
  if reserve_table_list_len != 1:
    global_variables.LOGGER.warning(f'Failed to get schedule - Expected 1 reserve table, got {reserve_table_list_len} instead')
    return {}

  reserve_table = reserve_table_list[0]
  if reserve_table.tbody is None:
    return {}

  reserve_table_rows = reserve_table.tbody.find_all('tr')
  reserve_table_rows_len = len(reserve_table_rows)
  if reserve_table_rows_len != 1:
    global_variables.LOGGER.warning(f'Failed to get schedule - Expected 1 schedule row, got {reserve_table_rows_len} rows instead')
    return {}

  reserve_table_datas = reserve_table_rows[0].find_all('td')
  if len(reserve_table_datas) == 0:
    global_variables.LOGGER.warning('Failed to get schedule - Table data is null')
    return {}

  # Get yesterday's date and update date at the start of each loop
  current_date = datetime.now().date() + timedelta(weeks=week) - timedelta(days=1)
  result_dict = {}
  for reserve_table_data in reserve_table_datas:
    current_date = current_date + timedelta(days=1)
    result_dict[current_date] = []
    reserve_table_data_div_list = reserve_table_data.find_all('div')
    if len(reserve_table_data_div_list) == 0:
      # Reserve table data div might be empty because schedule is only shown up to 1.5 weeks in advance
      continue

    for reserve_table_data_div in reserve_table_data_div_list:
      reserve_table_data_div_class_list = reserve_table_data_div.get('class')
      if len(reserve_table_data_div_class_list) < 2:
        availability = ClassAvailability.Null
      else:
        availability = RESPONSE_AVAILABILITY_MAP[reserve_table_data_div_class_list[1]]

      class_details = ClassData(
        studio=StudioType.AbsoluteSpin,
        location=StudioLocation.Null,
        name='',
        instructor='',
        time='',
        availability=availability,
        capacity_info=CapacityInfo())
      for reserve_table_data_div_span in reserve_table_data_div.find_all('span'):
        reserve_table_data_div_span_class_list = reserve_table_data_div_span.get('class')
        if len(reserve_table_data_div_span_class_list) == 0:
          global_variables.LOGGER.warning('Failed to get schedule - Table data span class is null')
          continue

        reserve_table_data_div_span_class = reserve_table_data_div_span_class_list[0]
        # scheduleSite span class is only provided if request has multiple locations
        if len(locations) == 1:
          class_details.location = locations[0]
        elif reserve_table_data_div_span_class == 'scheduleSite':
          location_str = str(reserve_table_data_div_span.contents[0].strip())
          class_details.location = LOCATION_STR_MAP[location_str]

        if reserve_table_data_div_span_class == 'scheduleClass':
          class_details.name = str(reserve_table_data_div_span.contents[0].strip())
        elif reserve_table_data_div_span_class == 'scheduleInstruc':
          class_details.instructor = str(reserve_table_data_div_span.contents[0].strip())
        elif reserve_table_data_div_span_class == 'scheduleTime':
          if len(class_details.name) == 0:
            continue

          class_details.set_time(str(reserve_table_data_div_span.contents[0].strip()))
          class_details.studio = StudioType.AbsoluteSpin if 'CYCLE' in class_details.name else StudioType.AbsolutePilates
          result_dict[current_date].append(copy(class_details))

    if len(result_dict[current_date]) == 0:
      result_dict.pop(current_date)

  return result_dict

def get_absolute_schedule() -> ResultData:
  def _get_absolute_schedule_internal(output_result: ResultData, locations: list[StudioLocation]) -> dict[datetime.date, list[ClassData]]:
    # REST API can only select one week at a time
    # Absolute schedule only shows up to 2 weeks in advance
    for week in range(0, 2):
      get_schedule_response = send_get_schedule_request(locations=locations, week=week)
      date_class_data_list_dict = parse_get_schedule_response(response=get_schedule_response, locations=locations, week=week)
      output_result.add_classes(date_class_data_list_dict)

  result = ResultData()
  # REST API can only select maximum of 5 locations at a time, but there are 6 locations
  location_map_list = list(LOCATION_MAP)
  _get_absolute_schedule_internal(result, location_map_list[0:1])
  _get_absolute_schedule_internal(result, location_map_list[1:])
  return result

def get_instructorid_map() -> dict[str, int]:
  def _get_instructorid_map_internal(response: requests.models.Response) -> dict[str, int]:
    soup = BeautifulSoup(response.text, 'html.parser')
    reserve_filters_list = [list_item for list_item in soup.find_all('ul') if list_item.get('id') == 'reserveFilter']
    reserve_filters_list_len = len(reserve_filters_list)
    if reserve_filters_list_len != 1:
      global_variables.LOGGER.warning(f'Failed to get list of instructors - Expected 1 reserve filter list, got {reserve_filters_list_len} instead')
      return {}

    reserve_filters = reserve_filters_list[0]
    instructor_filter_list = [list_item for list_item in reserve_filters.find_all('li') if list_item.get('id') == 'reserveFilter1']
    instructor_filter_list_len = len(instructor_filter_list)
    if instructor_filter_list_len != 1:
      global_variables.LOGGER.warning(f'Failed to get list of instructors - Expected 1 instructor filter list, got {instructor_filter_list_len} instead')
      return {}

    instructorid_map = {}
    instructorid_prefix = 'instructorid='
    instructorid_prefix_len = len(instructorid_prefix)
    instructorid_len = 19
    for instructor in instructor_filter_list[0].find_all('li'):
      instructor_name = instructor.string
      link = instructor.a.get('href')
      start_pos = link.find('instructorid=')
      instructorid = link[start_pos + instructorid_prefix_len:start_pos + instructorid_prefix_len + instructorid_len]
      instructorid_map[instructor_name.lower()] = instructorid
    return instructorid_map

  instructorid_map = {}
  location_map_list = list(LOCATION_MAP)

  # REST API can only select one week at a time
  # Absolute schedule only shows up to 2 weeks in advance
  for week in range(0, 2):
    get_schedule_response = send_get_schedule_request(locations=location_map_list[0:1], week=week)
    current_instructorid_map = _get_instructorid_map_internal(response=get_schedule_response)
    instructorid_map = {**instructorid_map, **current_instructorid_map}

    get_schedule_response = send_get_schedule_request(locations=location_map_list[1:], week=week)
    current_instructorid_map = _get_instructorid_map_internal(response=get_schedule_response)
    instructorid_map = {**instructorid_map, **current_instructorid_map}

  return instructorid_map
