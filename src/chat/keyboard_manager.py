"""
keyboard_manager.py
Author: https://github.com/lendrixxx
Description:
  This file defines the KeyboardManager class which is the main handler for the
  buttons used for interactions between the Telegram bot and the chats it is being used in.
"""

import telebot

from common.query_data import QueryData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


class KeyboardManager:
    """
    Manages button data for interactions between the Telegram bot and chats. This class
    handles query data, messages to be edited or deleted, and communication with users.

    Attributes:
      - main_page_keyboard (telebot.types.InlineKeyboardMarkup): Keyboard used for the main page.
      - studios_select_all_button (telebot.types.InlineKeyboardButton): Button for selecting all studios.
      - studios_unselect_all_button (telebot.types.InlineKeyboardButton): Button for unselecting all studios.
      - studios_buttons_unselected_map (dict[str, telebot.types.InlineKeyboardButton]):
        Dictionary of studios and unselected button for the studio.
      - studios_buttons_selected_map (dict[str, telebot.types.InlineKeyboardButton]):
        Dictionary of studios and selected button for the studio.
      - locations_select_all_button (telebot.types.InlineKeyboardButton): Button for selecting all locations.
      - locations_unselect_all_button (telebot.types.InlineKeyboardButton): Button for unselecting all locations
      - locations_select_more_studios_button (telebot.types.InlineKeyboardButton):
        Button for going back to studios selection from locations page.
      - studios_locations_buttons_unselected_map (dict[str, dict[str, telebot.types.InlineKeyboardButton]]):
        Dictionary of studios and dictionary of locations and unselected button for the location.
      - studios_locations_buttons_selected_map (dict[str, dict[str, telebot.types.InlineKeyboardButton]]):
        Dictionary of studios and dictionary of locations and selected button for the location.
      - rev_instructors_button (telebot.types.InlineKeyboardButton): Button to enter instructors for Rev.
      - barrys_instructors_button (telebot.types.InlineKeyboardButton): Button to enter instructors for Barrys.
      - absolute_spin_instructors_button (telebot.types.InlineKeyboardButton):
        Button to enter instructors for Absolute (Spin).
      - absolute_pilates_instructors_button (telebot.types.InlineKeyboardButton):
        Button to enter instructors for Absolute (Pilates).
      - ally_spin_instructors_button (telebot.types.InlineKeyboardButton):
        Button to enter instructors for Ally (Spin).
      - ally_pilates_instructors_button (telebot.types.InlineKeyboardButton):
        Button to enter instructors for Ally (Pilates).
      - anarchy_instructors_button (telebot.types.InlineKeyboardButton): Button to enter instructors for Anarchy.
      - show_instructors_button (telebot.types.InlineKeyboardButton): Button to show names of instructors.
      - next_button_to_main_page (telebot.types.InlineKeyboardButton): Next button to go to the main page.
      - weeks_page_keyboard (telebot.types.InlineKeyboardMarkup): Keyboard used for the weeks page.
      - days_select_all_button (telebot.types.InlineKeyboardButton): Button for selecting all days.
      - days_unselect_all_button (telebot.types.InlineKeyboardButton): Button for unselecting all days.
      - days_next_button (telebot.types.InlineKeyboardButton): Button for going to the next page from studios page.
      - days_buttons_unselected_map (dict[str, telebot.types.InlineKeyboardButton]):
        Dictionary of days and unselected button for the day.
      - days_buttons_selected_map (dict[str, telebot.types.InlineKeyboardButton]):
        Dictionary of days and selected button for the day.
      - timeslot_filter_keyboard (telebot.types.InlineKeyboardMarkup): Keyboard used for the timeslot filter page.
      - class_name_filter_keyboard (telebot.types.InlineKeyboardMarkup): Keyboard used for the class name filter page.

    """

    main_page_keyboard: telebot.types.InlineKeyboardMarkup
    studios_select_all_button: telebot.types.InlineKeyboardButton
    studios_unselect_all_button: telebot.types.InlineKeyboardButton
    studios_buttons_unselected_map: dict[str, telebot.types.InlineKeyboardButton]
    studios_buttons_selected_map: dict[str, telebot.types.InlineKeyboardButton]
    locations_select_all_button: telebot.types.InlineKeyboardButton
    locations_unselect_all_button: telebot.types.InlineKeyboardButton
    locations_select_more_studios_button: telebot.types.InlineKeyboardButton
    studios_locations_buttons_unselected_map: dict[str, dict[str, telebot.types.InlineKeyboardButton]]
    studios_locations_buttons_selected_map: dict[str, dict[str, telebot.types.InlineKeyboardButton]]
    rev_instructors_button: telebot.types.InlineKeyboardButton
    barrys_instructors_button: telebot.types.InlineKeyboardButton
    absolute_spin_instructors_button: telebot.types.InlineKeyboardButton
    absolute_pilates_instructors_button: telebot.types.InlineKeyboardButton
    ally_spin_instructors_button: telebot.types.InlineKeyboardButton
    ally_pilates_instructors_button: telebot.types.InlineKeyboardButton
    anarchy_instructors_button: telebot.types.InlineKeyboardButton
    show_instructors_button: telebot.types.InlineKeyboardButton
    next_button_to_main_page: telebot.types.InlineKeyboardButton
    weeks_page_keyboard: telebot.types.InlineKeyboardMarkup
    days_select_all_button: telebot.types.InlineKeyboardButton
    days_unselect_all_button: telebot.types.InlineKeyboardButton
    days_next_button: telebot.types.InlineKeyboardButton
    days_buttons_unselected_map: dict[str, telebot.types.InlineKeyboardButton]
    days_buttons_selected_map: dict[str, telebot.types.InlineKeyboardButton]
    timeslot_filter_keyboard: telebot.types.InlineKeyboardMarkup
    class_name_filter_keyboard: telebot.types.InlineKeyboardMarkup

    def __init__(self) -> None:
        """
        Initializes the KeyboardManager instance.
        """

        # Initialize main page keyboard
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
        get_schedule_button = telebot.types.InlineKeyboardButton(
            text="Get Schedule ▶️",
            callback_data="{'step': 'get-schedule'}",
        )

        self.main_page_keyboard = telebot.types.InlineKeyboardMarkup()
        self.main_page_keyboard.add(studios_button, instructors_button)
        self.main_page_keyboard.add(weeks_button, days_button)
        self.main_page_keyboard.add(time_button, class_name_button)
        self.main_page_keyboard.add(get_schedule_button)

        # Initialize studios buttons
        self.studios_select_all_button = telebot.types.InlineKeyboardButton(
            text="Select All",
            callback_data="{'studios': 'All', 'step': 'studios'}",
        )
        self.studios_unselect_all_button = telebot.types.InlineKeyboardButton(
            text="Unselect All",
            callback_data="{'studios': 'Null', 'step': 'studios'}",
        )
        self.studios_buttons_unselected_map = {
            "Rev": telebot.types.InlineKeyboardButton(
                text="Rev",
                callback_data="{'studios': 'Rev', 'step': 'studios'}",
            ),
            "Barrys": telebot.types.InlineKeyboardButton(
                text="Barrys",
                callback_data="{'studios': 'Barrys', 'step': 'studios'}",
            ),
            "Absolute (Spin)": telebot.types.InlineKeyboardButton(
                text="Absolute (Spin)",
                callback_data="{'studios': 'AbsoluteSpin', 'step': 'studios'}",
            ),
            "Absolute (Pilates)": telebot.types.InlineKeyboardButton(
                text="Absolute (Pilates)",
                callback_data="{'studios': 'AbsolutePilates', 'step': 'studios'}",
            ),
            "Ally (Spin)": telebot.types.InlineKeyboardButton(
                text="Ally (Spin)",
                callback_data="{'studios': 'AllySpin', 'step': 'studios'}",
            ),
            "Ally (Pilates)": telebot.types.InlineKeyboardButton(
                text="Ally (Pilates)",
                callback_data="{'studios': 'AllyPilates', 'step': 'studios'}",
            ),
            "Ally (Recovery)": telebot.types.InlineKeyboardButton(
                text="Ally (Recovery)",
                callback_data="{'studios': 'AllyRecovery', 'step': 'studios'}",
            ),
            "Anarchy": telebot.types.InlineKeyboardButton(
                text="Anarchy",
                callback_data="{'studios': 'Anarchy', 'step': 'studios'}",
            ),
        }
        self.studios_buttons_selected_map = {
            "Rev": telebot.types.InlineKeyboardButton(
                text="Rev ✅",
                callback_data="{'studios': 'Rev', 'step': 'studios'}",
            ),
            "Barrys": telebot.types.InlineKeyboardButton(
                text="Barrys ✅",
                callback_data="{'studios': 'Barrys', 'step': 'studios'}",
            ),
            "Absolute (Spin)": telebot.types.InlineKeyboardButton(
                text="Absolute (Spin) ✅",
                callback_data="{'studios': 'AbsoluteSpin', 'step': 'studios'}",
            ),
            "Absolute (Pilates)": telebot.types.InlineKeyboardButton(
                text="Absolute (Pilates) ✅",
                callback_data="{'studios': 'AbsolutePilates', 'step': 'studios'}",
            ),
            "Ally (Spin)": telebot.types.InlineKeyboardButton(
                text="Ally (Spin) ✅",
                callback_data="{'studios': 'AllySpin', 'step': 'studios'}",
            ),
            "Ally (Pilates)": telebot.types.InlineKeyboardButton(
                text="Ally (Pilates) ✅",
                callback_data="{'studios': 'AllyPilates', 'step': 'studios'}",
            ),
            "Ally (Recovery)": telebot.types.InlineKeyboardButton(
                text="Ally (Recovery) ✅",
                callback_data="{'studios': 'AllyRecovery', 'step': 'studios'}",
            ),
            "Anarchy": telebot.types.InlineKeyboardButton(
                text="Anarchy ✅",
                callback_data="{'studios': 'Anarchy', 'step': 'studios'}",
            ),
        }

        # Initialize locations buttons
        self.locations_select_all_button = telebot.types.InlineKeyboardButton(
            text="Select All",
            callback_data="{'location': 'All', 'step': 'locations'}",
        )
        self.locations_unselect_all_button = telebot.types.InlineKeyboardButton(
            text="Unselect All",
            callback_data="{'location': 'Null', 'step': 'locations'}",
        )
        self.locations_select_more_studios_button = telebot.types.InlineKeyboardButton(
            text="◀️ Select More",
            callback_data="{'step': 'studios-selection'}",
        )
        self.studios_locations_buttons_unselected_map = {
            "Rev": {
                "Bugis": telebot.types.InlineKeyboardButton(
                    text="Bugis",
                    callback_data="{'location': 'Bugis', 'step': 'locations'}",
                ),
                "Orchard": telebot.types.InlineKeyboardButton(
                    text="Orchard",
                    callback_data="{'location': 'Orchard', 'step': 'locations'}",
                ),
                "TJPG": telebot.types.InlineKeyboardButton(
                    text="TJPG",
                    callback_data="{'location': 'TJPG', 'step': 'locations'}",
                ),
            },
            "Barrys": {
                "Orchard": telebot.types.InlineKeyboardButton(
                    text="Orchard",
                    callback_data="{'location': 'Orchard', 'step': 'locations'}",
                ),
                "Raffles": telebot.types.InlineKeyboardButton(
                    text="Raffles",
                    callback_data="{'location': 'Raffles', 'step': 'locations'}",
                ),
            },
            "Absolute (Spin)": {
                "Centrepoint": telebot.types.InlineKeyboardButton(
                    text="Centrepoint",
                    callback_data="{'location': 'Centrepoint', 'step': 'locations'}",
                ),
                "i12": telebot.types.InlineKeyboardButton(
                    text="i12",
                    callback_data="{'location': 'i12', 'step': 'locations'}",
                ),
                "Star Vista": telebot.types.InlineKeyboardButton(
                    text="Star Vista",
                    callback_data="{'location': 'StarVista', 'step': 'locations'}",
                ),
                "Raffles": telebot.types.InlineKeyboardButton(
                    text="Raffles",
                    callback_data="{'location': 'Raffles', 'step': 'locations'}",
                ),
                "Millenia Walk": telebot.types.InlineKeyboardButton(
                    text="Millenia Walk",
                    callback_data="{'location': 'MilleniaWalk', 'step': 'locations'}",
                ),
            },
            "Absolute (Pilates)": {
                "Centrepoint": telebot.types.InlineKeyboardButton(
                    text="Centrepoint",
                    callback_data="{'location': 'Centrepoint', 'step': 'locations'}",
                ),
                "i12": telebot.types.InlineKeyboardButton(
                    text="i12",
                    callback_data="{'location': 'i12', 'step': 'locations'}",
                ),
                "Star Vista": telebot.types.InlineKeyboardButton(
                    text="Star Vista",
                    callback_data="{'location': 'StarVista', 'step': 'locations'}",
                ),
                "Raffles": telebot.types.InlineKeyboardButton(
                    text="Raffles",
                    callback_data="{'location': 'Raffles', 'step': 'locations'}",
                ),
                "Great World": telebot.types.InlineKeyboardButton(
                    text="Great World",
                    callback_data="{'location': 'GreatWorld', 'step': 'locations'}",
                ),
                "Millenia Walk": telebot.types.InlineKeyboardButton(
                    text="Millenia Walk",
                    callback_data="{'location': 'MilleniaWalk', 'step': 'locations'}",
                ),
            },
            "Ally (Spin)": {
                "Cross Street": telebot.types.InlineKeyboardButton(
                    text="Cross Street",
                    callback_data="{'location': 'CrossStreet', 'step': 'locations'}",
                ),
                "Maxwell": telebot.types.InlineKeyboardButton(
                    text="Maxwell",
                    callback_data="{'location': 'Maxwell', 'step': 'locations'}",
                ),
            },
            "Ally (Pilates)": {
                "Cross Street": telebot.types.InlineKeyboardButton(
                    text="Cross Street",
                    callback_data="{'location': 'CrossStreet', 'step': 'locations'}",
                ),
                "Maxwell": telebot.types.InlineKeyboardButton(
                    text="Maxwell",
                    callback_data="{'location': 'Maxwell', 'step': 'locations'}",
                ),
            },
            "Ally (Recovery)": {
                "Cross Street": telebot.types.InlineKeyboardButton(
                    text="Cross Street",
                    callback_data="{'location': 'CrossStreet', 'step': 'locations'}",
                ),
                "Maxwell": telebot.types.InlineKeyboardButton(
                    text="Maxwell",
                    callback_data="{'location': 'Maxwell', 'step': 'locations'}",
                ),
            },
            "Anarchy": {
                "Robinson": telebot.types.InlineKeyboardButton(
                    text="Robinson",
                    callback_data="{'location': 'Robinson', 'step': 'locations'}",
                ),
            },
        }
        self.studios_locations_buttons_selected_map = {
            "Rev": {
                "Bugis": telebot.types.InlineKeyboardButton(
                    text="Bugis ✅",
                    callback_data="{'location': 'Bugis', 'step': 'locations'}",
                ),
                "Orchard": telebot.types.InlineKeyboardButton(
                    text="Orchard ✅",
                    callback_data="{'location': 'Orchard', 'step': 'locations'}",
                ),
                "TJPG": telebot.types.InlineKeyboardButton(
                    text="TJPG ✅",
                    callback_data="{'location': 'TJPG', 'step': 'locations'}",
                ),
            },
            "Barrys": {
                "Orchard": telebot.types.InlineKeyboardButton(
                    text="Orchard ✅",
                    callback_data="{'location': 'Orchard', 'step': 'locations'}",
                ),
                "Raffles": telebot.types.InlineKeyboardButton(
                    text="Raffles ✅",
                    callback_data="{'location': 'Raffles', 'step': 'locations'}",
                ),
            },
            "Absolute (Spin)": {
                "Centrepoint": telebot.types.InlineKeyboardButton(
                    text="Centrepoint ✅",
                    callback_data="{'location': 'Centrepoint', 'step': 'locations'}",
                ),
                "i12": telebot.types.InlineKeyboardButton(
                    text="i12 ✅",
                    callback_data="{'location': 'i12', 'step': 'locations'}",
                ),
                "Star Vista": telebot.types.InlineKeyboardButton(
                    text="Star Vista ✅",
                    callback_data="{'location': 'StarVista', 'step': 'locations'}",
                ),
                "Raffles": telebot.types.InlineKeyboardButton(
                    text="Raffles ✅",
                    callback_data="{'location': 'Raffles', 'step': 'locations'}",
                ),
                "Millenia Walk": telebot.types.InlineKeyboardButton(
                    text="Millenia Walk ✅",
                    callback_data="{'location': 'MilleniaWalk', 'step': 'locations'}",
                ),
            },
            "Absolute (Pilates)": {
                "Centrepoint": telebot.types.InlineKeyboardButton(
                    text="Centrepoint ✅",
                    callback_data="{'location': 'Centrepoint', 'step': 'locations'}",
                ),
                "i12": telebot.types.InlineKeyboardButton(
                    text="i12 ✅",
                    callback_data="{'location': 'i12', 'step': 'locations'}",
                ),
                "Star Vista": telebot.types.InlineKeyboardButton(
                    text="Star Vista ✅",
                    callback_data="{'location': 'StarVista', 'step': 'locations'}",
                ),
                "Raffles": telebot.types.InlineKeyboardButton(
                    text="Raffles ✅",
                    callback_data="{'location': 'Raffles', 'step': 'locations'}",
                ),
                "Great World": telebot.types.InlineKeyboardButton(
                    text="Great World ✅",
                    callback_data="{'location': 'GreatWorld', 'step': 'locations'}",
                ),
                "Millenia Walk": telebot.types.InlineKeyboardButton(
                    text="Millenia Walk ✅",
                    callback_data="{'location': 'MilleniaWalk', 'step': 'locations'}",
                ),
            },
            "Ally (Spin)": {
                "Cross Street": telebot.types.InlineKeyboardButton(
                    text="Cross Street ✅",
                    callback_data="{'location': 'CrossStreet', 'step': 'locations'}",
                ),
                "Maxwell": telebot.types.InlineKeyboardButton(
                    text="Maxwell ✅",
                    callback_data="{'location': 'Maxwell', 'step': 'locations'}",
                ),
            },
            "Ally (Pilates)": {
                "Cross Street": telebot.types.InlineKeyboardButton(
                    text="Cross Street ✅",
                    callback_data="{'location': 'CrossStreet', 'step': 'locations'}",
                ),
                "Maxwell": telebot.types.InlineKeyboardButton(
                    text="Maxwell ✅",
                    callback_data="{'location': 'Maxwell', 'step': 'locations'}",
                ),
            },
            "Ally (Recovery)": {
                "Cross Street": telebot.types.InlineKeyboardButton(
                    text="Cross Street ✅",
                    callback_data="{'location': 'CrossStreet', 'step': 'locations'}",
                ),
                "Maxwell": telebot.types.InlineKeyboardButton(
                    text="Maxwell ✅",
                    callback_data="{'location': 'Maxwell', 'step': 'locations'}",
                ),
            },
            "Anarchy": {
                "Robinson": telebot.types.InlineKeyboardButton(
                    text="Robinson ✅",
                    callback_data="{'location': 'Robinson', 'step': 'locations'}",
                ),
            },
        }

        # Initialize instructors buttons
        self.rev_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Rev Instructor(s)",
            callback_data="{'step': 'rev-instructors'}",
        )
        self.barrys_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Barrys Instructor(s)",
            callback_data="{'step': 'barrys-instructors'}",
        )
        self.absolute_spin_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Absolute (Spin) Instructor(s)",
            callback_data="{'step': 'absolute-spin-instructors'}",
        )
        self.absolute_pilates_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Absolute (Pilates) Instructor(s)",
            callback_data="{'step': 'absolute-pilates-instructors'}",
        )
        self.ally_spin_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Ally (Spin) Instructor(s)",
            callback_data="{'step': 'ally-spin-instructors'}",
        )
        self.ally_pilates_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Ally (Pilates) Instructor(s)",
            callback_data="{'step': 'ally-pilates-instructors'}",
        )
        self.anarchy_instructors_button = telebot.types.InlineKeyboardButton(
            text="Enter Anarchy Instructor(s)",
            callback_data="{'step': 'anarchy-instructors'}",
        )
        self.show_instructors_button = telebot.types.InlineKeyboardButton(
            text="Show Names of Instructors",
            callback_data="{'step': 'show-instructors'}",
        )
        self.next_button_to_main_page = telebot.types.InlineKeyboardButton(
            text="Next ▶️",
            callback_data="{'step': 'main-page-handler'}",
        )

        # Initialize weeks keyboard
        one_button = telebot.types.InlineKeyboardButton(text="1", callback_data="{'weeks': 1, 'step': 'weeks'}")
        two_button = telebot.types.InlineKeyboardButton(text="2", callback_data="{'weeks': 2, 'step': 'weeks'}")
        three_button = telebot.types.InlineKeyboardButton(text="3", callback_data="{'weeks': 3, 'step': 'weeks'}")
        four_button = telebot.types.InlineKeyboardButton(text="4", callback_data="{'weeks': 4, 'step': 'weeks'}")
        back_button = telebot.types.InlineKeyboardButton(text="◀️ Back", callback_data="{'step': 'main-page-handler'}")

        self.weeks_page_keyboard = telebot.types.InlineKeyboardMarkup()
        self.weeks_page_keyboard.add(one_button, two_button)
        self.weeks_page_keyboard.add(three_button, four_button)
        self.weeks_page_keyboard.add(back_button)

        # Initialize days buttons
        self.days_select_all_button = telebot.types.InlineKeyboardButton(
            text="Select All",
            callback_data="{'days': 'All', 'step': 'days'}",
        )
        self.days_unselect_all_button = telebot.types.InlineKeyboardButton(
            text="Unselect All",
            callback_data="{'days': 'None', 'step': 'days'}",
        )
        self.days_next_button = telebot.types.InlineKeyboardButton(
            text="Next ▶️",
            callback_data="{'step': 'days-next'}",
        )
        self.days_buttons_unselected_map = {
            "Monday": telebot.types.InlineKeyboardButton(
                text="Monday",
                callback_data="{'days': 'Monday', 'step': 'days'}",
            ),
            "Tuesday": telebot.types.InlineKeyboardButton(
                text="Tuesday",
                callback_data="{'days': 'Tuesday', 'step': 'days'}",
            ),
            "Wednesday": telebot.types.InlineKeyboardButton(
                text="Wednesday",
                callback_data="{'days': 'Wednesday', 'step': 'days'}",
            ),
            "Thursday": telebot.types.InlineKeyboardButton(
                text="Thursday",
                callback_data="{'days': 'Thursday', 'step': 'days'}",
            ),
            "Friday": telebot.types.InlineKeyboardButton(
                text="Friday",
                callback_data="{'days': 'Friday', 'step': 'days'}",
            ),
            "Saturday": telebot.types.InlineKeyboardButton(
                text="Saturday",
                callback_data="{'days': 'Saturday', 'step': 'days'}",
            ),
            "Sunday": telebot.types.InlineKeyboardButton(
                text="Sunday",
                callback_data="{'days': 'Sunday', 'step': 'days'}",
            ),
        }
        self.days_buttons_selected_map = {
            "Monday": telebot.types.InlineKeyboardButton(
                text="Monday ✅",
                callback_data="{'days': 'Monday', 'step': 'days'}",
            ),
            "Tuesday": telebot.types.InlineKeyboardButton(
                text="Tuesday ✅",
                callback_data="{'days': 'Tuesday', 'step': 'days'}",
            ),
            "Wednesday": telebot.types.InlineKeyboardButton(
                text="Wednesday ✅",
                callback_data="{'days': 'Wednesday', 'step': 'days'}",
            ),
            "Thursday": telebot.types.InlineKeyboardButton(
                text="Thursday ✅",
                callback_data="{'days': 'Thursday', 'step': 'days'}",
            ),
            "Friday": telebot.types.InlineKeyboardButton(
                text="Friday ✅",
                callback_data="{'days': 'Friday', 'step': 'days'}",
            ),
            "Saturday": telebot.types.InlineKeyboardButton(
                text="Saturday ✅",
                callback_data="{'days': 'Saturday', 'step': 'days'}",
            ),
            "Sunday": telebot.types.InlineKeyboardButton(
                text="Sunday ✅",
                callback_data="{'days': 'Sunday', 'step': 'days'}",
            ),
        }

        # Initialize timeslot filter keyboard
        self.timeslot_filter_keyboard = telebot.types.InlineKeyboardMarkup()
        add_timeslot_button = telebot.types.InlineKeyboardButton(
            text="Add Timeslot",
            callback_data="{'step': 'time-selection-add'}",
        )
        remove_timeslot_button = telebot.types.InlineKeyboardButton(
            text="Remove Timeslot",
            callback_data="{'step': 'time-selection-remove'}",
        )
        reset_all_timeslot_button = telebot.types.InlineKeyboardButton(
            text="Reset All Timeslot(s)",
            callback_data="{'step': 'time-selection-reset'}",
        )

        self.timeslot_filter_keyboard = telebot.types.InlineKeyboardMarkup()
        self.timeslot_filter_keyboard.add(add_timeslot_button)
        self.timeslot_filter_keyboard.add(remove_timeslot_button)
        self.timeslot_filter_keyboard.add(reset_all_timeslot_button)
        self.timeslot_filter_keyboard.add(self.next_button_to_main_page)

        # Initialize class name filter keyboard
        self.class_name_filter_keyboard = telebot.types.InlineKeyboardMarkup()
        set_filter_button = telebot.types.InlineKeyboardButton(
            text="Add Filter",
            callback_data="{'step': 'class-name-filter-add'}",
        )
        reset_filter_button = telebot.types.InlineKeyboardButton(
            text="Reset Filter",
            callback_data="{'step': 'class-name-filter-reset'}",
        )

        self.class_name_filter_keyboard = telebot.types.InlineKeyboardMarkup()
        self.class_name_filter_keyboard.add(set_filter_button, reset_filter_button)
        self.class_name_filter_keyboard.add(self.next_button_to_main_page)

    def get_main_page_keyboard(self) -> telebot.types.InlineKeyboardMarkup:
        """
        Returns the keyboard to be used for the main page.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        return self.main_page_keyboard

    def get_studios_keyboard(self, query: QueryData) -> telebot.types.InlineKeyboardMarkup:
        """
        Constructs the studios keyboard to be used based on the specified query.

        Args:
          - query (QueryData): The query data to construct the studios keyboard for.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        studios_keyboard = telebot.types.InlineKeyboardMarkup()

        studio_buttons = {
            StudioType.Rev: self.studios_buttons_unselected_map["Rev"],
            StudioType.Barrys: self.studios_buttons_unselected_map["Barrys"],
            StudioType.AbsoluteSpin: self.studios_buttons_unselected_map["Absolute (Spin)"],
            StudioType.AbsolutePilates: self.studios_buttons_unselected_map["Absolute (Pilates)"],
            StudioType.AllySpin: self.studios_buttons_unselected_map["Ally (Spin)"],
            StudioType.AllyPilates: self.studios_buttons_unselected_map["Ally (Pilates)"],
            StudioType.AllyRecovery: self.studios_buttons_unselected_map["Ally (Recovery)"],
            StudioType.Anarchy: self.studios_buttons_unselected_map["Anarchy"],
        }

        for studio in studio_buttons:
            if studio in query.studios:
                studio_buttons[studio] = self.studios_buttons_selected_map[studio.value]

        studios_keyboard.add(studio_buttons[StudioType.Rev], studio_buttons[StudioType.Barrys])
        studios_keyboard.add(studio_buttons[StudioType.AbsoluteSpin], studio_buttons[StudioType.AbsolutePilates])
        studios_keyboard.add(studio_buttons[StudioType.AllySpin], studio_buttons[StudioType.AllyPilates])
        studios_keyboard.add(studio_buttons[StudioType.AllyRecovery], studio_buttons[StudioType.Anarchy])
        studios_keyboard.add(self.studios_select_all_button, self.studios_unselect_all_button)
        studios_keyboard.add(self.next_button_to_main_page)
        return studios_keyboard

    def get_locations_keyboard(self, query: QueryData) -> telebot.types.InlineKeyboardMarkup:
        """
        Constructs the locations keyboard to be used based on the specified query.

        Args:
          - query (QueryData): The query data to construct the locations keyboard for.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        locations_keyboard = telebot.types.InlineKeyboardMarkup()
        studio_locations_buttons = {
            StudioType.Rev: {
                StudioLocation.Bugis: self.studios_locations_buttons_unselected_map["Rev"]["Bugis"],
                StudioLocation.Orchard: self.studios_locations_buttons_unselected_map["Rev"]["Orchard"],
                StudioLocation.TJPG: self.studios_locations_buttons_unselected_map["Rev"]["TJPG"],
            },
            StudioType.Barrys: {
                StudioLocation.Orchard: self.studios_locations_buttons_unselected_map["Barrys"]["Orchard"],
                StudioLocation.Raffles: self.studios_locations_buttons_unselected_map["Barrys"]["Raffles"],
            },
            StudioType.AllySpin: {
                StudioLocation.CrossStreet: self.studios_locations_buttons_unselected_map["Ally (Spin)"][
                    "Cross Street"
                ],
                StudioLocation.Maxwell: self.studios_locations_buttons_unselected_map["Ally (Spin)"]["Maxwell"],
            },
            StudioType.AllyPilates: {
                StudioLocation.CrossStreet: self.studios_locations_buttons_unselected_map["Ally (Pilates)"][
                    "Cross Street"
                ],
                StudioLocation.Maxwell: self.studios_locations_buttons_unselected_map["Ally (Pilates)"]["Maxwell"],
            },
            StudioType.AllyRecovery: {
                StudioLocation.CrossStreet: self.studios_locations_buttons_unselected_map["Ally (Recovery)"][
                    "Cross Street"
                ],
                StudioLocation.Maxwell: self.studios_locations_buttons_unselected_map["Ally (Recovery)"]["Maxwell"],
            },
            StudioType.AbsoluteSpin: {
                StudioLocation.Centrepoint: self.studios_locations_buttons_unselected_map["Absolute (Spin)"][
                    "Centrepoint"
                ],
                StudioLocation.i12: self.studios_locations_buttons_unselected_map["Absolute (Spin)"]["i12"],
                StudioLocation.StarVista: self.studios_locations_buttons_unselected_map["Absolute (Spin)"][
                    "Star Vista"
                ],
                StudioLocation.Raffles: self.studios_locations_buttons_unselected_map["Absolute (Spin)"]["Raffles"],
                StudioLocation.MilleniaWalk: self.studios_locations_buttons_unselected_map["Absolute (Spin)"][
                    "Millenia Walk"
                ],
            },
            StudioType.AbsolutePilates: {
                StudioLocation.Centrepoint: self.studios_locations_buttons_unselected_map["Absolute (Pilates)"][
                    "Centrepoint"
                ],
                StudioLocation.i12: self.studios_locations_buttons_unselected_map["Absolute (Pilates)"]["i12"],
                StudioLocation.StarVista: self.studios_locations_buttons_unselected_map["Absolute (Pilates)"][
                    "Star Vista"
                ],
                StudioLocation.Raffles: self.studios_locations_buttons_unselected_map["Absolute (Pilates)"]["Raffles"],
                StudioLocation.GreatWorld: self.studios_locations_buttons_unselected_map["Absolute (Pilates)"][
                    "Great World"
                ],
                StudioLocation.MilleniaWalk: self.studios_locations_buttons_unselected_map["Absolute (Pilates)"][
                    "Millenia Walk"
                ],
            },
        }

        if query.current_studio in query.studios:
            current_studio_data = query.studios[query.current_studio]
            for location in studio_locations_buttons[query.current_studio]:
                if location in current_studio_data.locations:
                    studio_locations_buttons[query.current_studio][location] = (
                        self.studios_locations_buttons_selected_map[query.current_studio.value][location.value]
                    )

        if query.current_studio == "Rev":
            locations_keyboard.add(studio_locations_buttons["Rev"]["Bugis"], studio_locations_buttons["Rev"]["Orchard"])
            locations_keyboard.add(studio_locations_buttons["Rev"]["TJPG"])
        elif query.current_studio == "Barrys":
            locations_keyboard.add(
                studio_locations_buttons["Barrys"]["Orchard"],
                studio_locations_buttons["Barrys"]["Raffles"],
            )
        elif query.current_studio == "Ally (Spin)":
            locations_keyboard.add(
                studio_locations_buttons["Ally (Spin)"]["Cross Street"],
                studio_locations_buttons["Ally (Spin)"]["Maxwell"],
            )
        elif query.current_studio == "Ally (Pilates)":
            locations_keyboard.add(
                studio_locations_buttons["Ally (Pilates)"]["Cross Street"],
                studio_locations_buttons["Ally (Pilates)"]["Maxwell"],
            )
        elif query.current_studio == "Ally (Recovery)":
            locations_keyboard.add(
                studio_locations_buttons["Ally (Recovery)"]["Cross Street"],
                studio_locations_buttons["Ally (Recovery)"]["Maxwell"],
            )
        elif query.current_studio == "Absolute (Spin)":
            locations_keyboard.add(
                studio_locations_buttons["Absolute (Spin)"]["Centrepoint"],
                studio_locations_buttons["Absolute (Spin)"]["i12"],
            )
            locations_keyboard.add(
                studio_locations_buttons["Absolute (Spin)"]["Star Vista"],
                studio_locations_buttons["Absolute (Spin)"]["Raffles"],
            )
            locations_keyboard.add(studio_locations_buttons["Absolute (Spin)"]["Millenia Walk"])
        elif query.current_studio == "Absolute (Pilates)":
            locations_keyboard.add(
                studio_locations_buttons["Absolute (Pilates)"]["Centrepoint"],
                studio_locations_buttons["Absolute (Pilates)"]["i12"],
            )
            locations_keyboard.add(
                studio_locations_buttons["Absolute (Pilates)"]["Star Vista"],
                studio_locations_buttons["Absolute (Pilates)"]["Raffles"],
            )
            locations_keyboard.add(
                studio_locations_buttons["Absolute (Pilates)"]["Millenia Walk"],
                studio_locations_buttons["Absolute (Pilates)"]["Great World"],
            )
        locations_keyboard.add(self.locations_select_all_button, self.locations_unselect_all_button)
        locations_keyboard.add(self.locations_select_more_studios_button, self.next_button_to_main_page)
        return locations_keyboard

    def get_instructors_keyboard(self, query: QueryData) -> telebot.types.InlineKeyboardMarkup:
        """
        Constructs the instructors keyboard to be used based on the specified query.

        Args:
          - query (QueryData): The query data to construct the days keyboard for.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        instructors_keyboard = telebot.types.InlineKeyboardMarkup()
        if StudioType.Rev in query.studios:
            instructors_keyboard.add(self.rev_instructors_button)
        if StudioType.Barrys in query.studios:
            instructors_keyboard.add(self.barrys_instructors_button)
        if StudioType.AbsoluteSpin in query.studios:
            instructors_keyboard.add(self.absolute_spin_instructors_button)
        if StudioType.AbsolutePilates in query.studios:
            instructors_keyboard.add(self.absolute_pilates_instructors_button)
        if StudioType.AllySpin in query.studios:
            instructors_keyboard.add(self.ally_spin_instructors_button)
        if StudioType.AllyPilates in query.studios:
            instructors_keyboard.add(self.ally_pilates_instructors_button)
        if StudioType.Anarchy in query.studios:
            instructors_keyboard.add(self.anarchy_instructors_button)

        instructors_keyboard.add(self.show_instructors_button)
        instructors_keyboard.add(self.next_button_to_main_page)
        return instructors_keyboard

    def get_weeks_page_keyboard(self) -> telebot.types.InlineKeyboardMarkup:
        """
        Returns the keyboard to be used for the weeks page.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        return self.weeks_page_keyboard

    def get_days_keyboard(self, query: QueryData) -> telebot.types.InlineKeyboardMarkup:
        """
        Constructs the days keyboard to be used based on the specified query.

        Args:
          - query (QueryData): The query data to construct the days keyboard for.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        days_keyboard = telebot.types.InlineKeyboardMarkup()

        days_buttons = {
            "Monday": self.days_buttons_unselected_map["Monday"],
            "Tuesday": self.days_buttons_unselected_map["Tuesday"],
            "Wednesday": self.days_buttons_unselected_map["Wednesday"],
            "Thursday": self.days_buttons_unselected_map["Thursday"],
            "Friday": self.days_buttons_unselected_map["Friday"],
            "Saturday": self.days_buttons_unselected_map["Saturday"],
            "Sunday": self.days_buttons_unselected_map["Sunday"],
        }

        for day in days_buttons:
            if day in query.days:
                days_buttons[day] = self.days_buttons_selected_map[day]

        days_keyboard.add(days_buttons["Monday"], days_buttons["Tuesday"])
        days_keyboard.add(days_buttons["Wednesday"], days_buttons["Thursday"])
        days_keyboard.add(days_buttons["Friday"], days_buttons["Saturday"])
        days_keyboard.add(days_buttons["Sunday"])
        days_keyboard.add(self.days_select_all_button, self.days_unselect_all_button)
        days_keyboard.add(self.days_next_button)
        return days_keyboard

    def get_timeslot_filter_keyboard(self) -> telebot.types.InlineKeyboardMarkup:
        """
        Returns the keyboard to be used for the timeslot filter page.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        return self.timeslot_filter_keyboard

    def get_class_name_filter_keyboard(self) -> telebot.types.InlineKeyboardMarkup:
        """
        Returns the keyboard to be used for the class name filter page.

        Returns:
          telebot.types.InlineKeyboardMarkup: The keyboard to be used.

        """
        return self.class_name_filter_keyboard
