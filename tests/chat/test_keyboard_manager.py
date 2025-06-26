"""
test_keyboard_manager.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the KeyboardManager class.
"""

from typing import NamedTuple

import pytest

from chat.keyboard_manager import KeyboardManager
from common.query_data import QueryData
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


class KeyboardButtonArgs(NamedTuple):
    keyboard_name: str
    rows_number_of_buttons_list: list[int]
    expected_buttons_texts_and_callback_data: list[tuple[str, str]]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            KeyboardButtonArgs(
                keyboard_name="main_page_keyboard",
                rows_number_of_buttons_list=[
                    2,  # Studios, Instructors
                    2,  # Weeks, Days
                    2,  # Time, Class Name
                    1,  # Get Schedule
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Studios", "{'step': 'studios-selection'}"),
                    ("Instructors", "{'step': 'instructors-selection'}"),
                    ("Weeks", "{'step': 'weeks-selection'}"),
                    ("Days", "{'step': 'days-selection'}"),
                    ("Time", "{'step': 'time-selection'}"),
                    ("Class Name", "{'step': 'class-name-filter-selection'}"),
                    ("Get Schedule ▶️", "{'step': 'get-schedule'}"),
                ],
            ),
            id="Main page keyboard",
        ),
        pytest.param(
            KeyboardButtonArgs(
                keyboard_name="weeks_page_keyboard",
                rows_number_of_buttons_list=[
                    2,  # 1, 2
                    2,  # 3, 4
                    1,  # Back
                ],
                expected_buttons_texts_and_callback_data=[
                    ("1", "{'weeks': 1, 'step': 'weeks'}"),
                    ("2", "{'weeks': 2, 'step': 'weeks'}"),
                    ("3", "{'weeks': 3, 'step': 'weeks'}"),
                    ("4", "{'weeks': 4, 'step': 'weeks'}"),
                    ("◀️ Back", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Weeks page keyboard",
        ),
        pytest.param(
            KeyboardButtonArgs(
                keyboard_name="timeslot_filter_keyboard",
                rows_number_of_buttons_list=[
                    1,  # Add Timeslot
                    1,  # Remove Timeslot
                    1,  # Reset All Timeslot(s)
                    1,  # Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Add Timeslot", "{'step': 'time-selection-add'}"),
                    ("Remove Timeslot", "{'step': 'time-selection-remove'}"),
                    ("Reset All Timeslot(s)", "{'step': 'time-selection-reset'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Timeslot filter keyboard",
        ),
        pytest.param(
            KeyboardButtonArgs(
                keyboard_name="class_name_filter_keyboard",
                rows_number_of_buttons_list=[
                    2,  # Add Filter, Reset Filter
                    1,  # Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Add Filter", "{'step': 'class-name-filter-add'}"),
                    ("Reset Filter", "{'step': 'class-name-filter-reset'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Class name filter keyboard",
        ),
    ],
)
def test_keyboard_buttons(args: KeyboardButtonArgs) -> None:
    """
    Tests that the keyboards in KeyboardManager is initialized with the correct buttons.

    Args:
      - args (KeyboardButtonArgs): Provides arguments for the test case.

    """
    keyboard_manager = KeyboardManager()
    keyboard = getattr(keyboard_manager, args.keyboard_name)

    # Assert button layout rows
    assert len(keyboard.keyboard) == len(args.rows_number_of_buttons_list)
    for keyboard_list, number_of_buttons in zip(keyboard.keyboard, args.rows_number_of_buttons_list):
        assert len(keyboard_list) == number_of_buttons

    # Assert button texts and callback data
    button_texts = [button.text for row in keyboard.keyboard for button in row]
    callback_data = [button.callback_data for row in keyboard.keyboard for button in row]

    for (expected_text, expected_callback), actual_text, actual_callback in zip(
        args.expected_buttons_texts_and_callback_data, button_texts, callback_data
    ):
        assert actual_text == expected_text
        assert actual_callback == expected_callback


class GetStudiosKeyboardArgs(NamedTuple):
    selected_studios: dict[StudioType, StudioData]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetStudiosKeyboardArgs(
                selected_studios={StudioType.Rev: StudioData()},
            ),
            id="Rev selected",
        ),
        pytest.param(
            GetStudiosKeyboardArgs(
                selected_studios={
                    StudioType.AbsoluteSpin: StudioData(),
                    StudioType.AbsolutePilates: StudioData(),
                    StudioType.AllySpin: StudioData(),
                    StudioType.AllyPilates: StudioData(),
                    StudioType.AllyRecovery: StudioData(),
                    StudioType.Anarchy: StudioData(),
                    StudioType.Barrys: StudioData(),
                    StudioType.Rev: StudioData(),
                },
            ),
            id="All selected",
        ),
        pytest.param(
            GetStudiosKeyboardArgs(
                selected_studios={},
            ),
            id="None selected",
        ),
        pytest.param(
            GetStudiosKeyboardArgs(
                selected_studios={
                    StudioType.AbsolutePilates: StudioData(),
                    StudioType.AllySpin: StudioData(),
                    StudioType.Anarchy: StudioData(),
                    StudioType.Barrys: StudioData(),
                },
            ),
            id="Ally (Spin), Absolute (Pilates), Anarchy, and Barrys selected",
        ),
    ],
)
def test_get_studios_keyboard(
    args: GetStudiosKeyboardArgs,
    sample_query_data: QueryData,
) -> None:
    """
    Test the get_studios_keyboard method to ensure the correct buttons are selected
    based on the query data.

    Args:
      - args (GetStudiosKeyboardArgs): Provides arguments for the test case.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    keyboard_manager = KeyboardManager()

    sample_query_data.studios = args.selected_studios

    # Call the function to test
    keyboard = keyboard_manager.get_studios_keyboard(sample_query_data)

    # Assert that the response is as expected
    assert len(keyboard.keyboard) == 6
    assert len(keyboard.keyboard[0]) == 2  # Rev, Barrys
    assert len(keyboard.keyboard[1]) == 2  # Absolute (Spin), Absolute (Pilates)
    assert len(keyboard.keyboard[2]) == 2  # Ally (Spin), Ally (Pilates)
    assert len(keyboard.keyboard[3]) == 2  # All (Recovery), Anarchy
    assert len(keyboard.keyboard[4]) == 2  # Select All, Unselect All
    assert len(keyboard.keyboard[5]) == 1  # Next
    actual_button_data_map = {
        StudioType.Rev: (keyboard.keyboard[0][0].text, keyboard.keyboard[0][0].callback_data),
        StudioType.Barrys: (keyboard.keyboard[0][1].text, keyboard.keyboard[0][1].callback_data),
        StudioType.AbsoluteSpin: (keyboard.keyboard[1][0].text, keyboard.keyboard[1][0].callback_data),
        StudioType.AbsolutePilates: (keyboard.keyboard[1][1].text, keyboard.keyboard[1][1].callback_data),
        StudioType.AllySpin: (keyboard.keyboard[2][0].text, keyboard.keyboard[2][0].callback_data),
        StudioType.AllyPilates: (keyboard.keyboard[2][1].text, keyboard.keyboard[2][1].callback_data),
        StudioType.AllyRecovery: (keyboard.keyboard[3][0].text, keyboard.keyboard[3][0].callback_data),
        StudioType.Anarchy: (keyboard.keyboard[3][1].text, keyboard.keyboard[3][1].callback_data),
    }

    # Loop through button data and assert the correct selected/unselected buttons
    for studio, (actual_button_text, actual_button_callback_data) in actual_button_data_map.items():
        assert actual_button_callback_data == f"{{'studios': '{studio.name}', 'step': 'studios'}}"
        if studio in args.selected_studios:
            assert actual_button_text == f"{studio.value} ✅"
        else:
            assert actual_button_text == f"{studio.value}"


class GetLocationsKeyboardArgs(NamedTuple):
    current_studio: StudioType
    selected_studios: dict[StudioType, StudioData]
    rows_number_of_buttons_list: list[int]
    expected_buttons_texts_and_callback_data: list[tuple[str, str]]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.Rev,
                selected_studios={StudioType.Rev: StudioData()},
                rows_number_of_buttons_list=[
                    2,  # Bugis, Orchard
                    1,  # TJPG
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Bugis", "{'location': 'Bugis', 'step': 'locations'}"),
                    ("Orchard", "{'location': 'Orchard', 'step': 'locations'}"),
                    ("TJPG", "{'location': 'TJPG', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Rev with no location selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.Rev,
                selected_studios={StudioType.Rev: StudioData(locations=[StudioLocation.Bugis])},
                rows_number_of_buttons_list=[
                    2,  # Bugis, Orchard
                    1,  # TJPG
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Bugis ✅", "{'location': 'Bugis', 'step': 'locations'}"),
                    ("Orchard", "{'location': 'Orchard', 'step': 'locations'}"),
                    ("TJPG", "{'location': 'TJPG', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Rev with Bugis selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.Barrys,
                selected_studios={
                    StudioType.Barrys: StudioData(locations=[StudioLocation.Orchard, StudioLocation.Raffles]),
                },
                rows_number_of_buttons_list=[
                    2,  # Orchard, Raffles
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Orchard ✅", "{'location': 'Orchard', 'step': 'locations'}"),
                    ("Raffles ✅", "{'location': 'Raffles', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Barrys with Orchard and Raffles selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.AbsoluteSpin,
                selected_studios={
                    StudioType.AbsoluteSpin: StudioData(),
                },
                rows_number_of_buttons_list=[
                    2,  # Centrepoint, i12
                    2,  # Star Vista, Raffles
                    1,  # Millenia Walk
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Centrepoint", "{'location': 'Centrepoint', 'step': 'locations'}"),
                    ("i12", "{'location': 'i12', 'step': 'locations'}"),
                    ("Star Vista", "{'location': 'StarVista', 'step': 'locations'}"),
                    ("Raffles", "{'location': 'Raffles', 'step': 'locations'}"),
                    ("Millenia Walk", "{'location': 'MilleniaWalk', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Absolute (Spin) with no location selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.AbsolutePilates,
                selected_studios={
                    StudioType.AbsolutePilates: StudioData(),
                },
                rows_number_of_buttons_list=[
                    2,  # Centrepoint, i12
                    2,  # Star Vista, Raffles
                    2,  # Millenia Walk, Great World
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Centrepoint", "{'location': 'Centrepoint', 'step': 'locations'}"),
                    ("i12", "{'location': 'i12', 'step': 'locations'}"),
                    ("Star Vista", "{'location': 'StarVista', 'step': 'locations'}"),
                    ("Raffles", "{'location': 'Raffles', 'step': 'locations'}"),
                    ("Millenia Walk", "{'location': 'MilleniaWalk', 'step': 'locations'}"),
                    ("Great World", "{'location': 'GreatWorld', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Absolute (Pilates) with no location selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.AllySpin,
                selected_studios={
                    StudioType.AllySpin: StudioData(locations=[StudioLocation.CrossStreet]),
                },
                rows_number_of_buttons_list=[
                    2,  # Cross Street, Maxwell
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Cross Street ✅", "{'location': 'CrossStreet', 'step': 'locations'}"),
                    ("Maxwell", "{'location': 'Maxwell', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Ally (Spin) with Cross Street selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.AllyPilates,
                selected_studios={
                    StudioType.AllyPilates: StudioData(locations=[StudioLocation.Maxwell]),
                },
                rows_number_of_buttons_list=[
                    2,  # Cross Street, Maxwell
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Cross Street", "{'location': 'CrossStreet', 'step': 'locations'}"),
                    ("Maxwell ✅", "{'location': 'Maxwell', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Ally (Pilates) with Maxwell selected",
        ),
        pytest.param(
            GetLocationsKeyboardArgs(
                current_studio=StudioType.AllyRecovery,
                selected_studios={
                    StudioType.AllyRecovery: StudioData(locations=[StudioLocation.CrossStreet, StudioLocation.Maxwell]),
                },
                rows_number_of_buttons_list=[
                    2,  # Cross Street, Maxwell
                    2,  # Select All, Unselect All
                    2,  # Select More, Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Cross Street ✅", "{'location': 'CrossStreet', 'step': 'locations'}"),
                    ("Maxwell ✅", "{'location': 'Maxwell', 'step': 'locations'}"),
                    ("Select All", "{'location': 'All', 'step': 'locations'}"),
                    ("Unselect All", "{'location': 'Null', 'step': 'locations'}"),
                    ("◀️ Select More", "{'step': 'studios-selection'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Ally (Recovery) with Cross Street and Maxwell selected",
        ),
    ],
)
def test_get_locations_keyboard(
    args: GetLocationsKeyboardArgs,
    sample_query_data: QueryData,
) -> None:
    """
    Test the get_locations_keyboard method to ensure the correct buttons are selected
    based on the query data.

    Args:
      - args (GetLocationsKeyboardArgs): Provides arguments for the test case.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    keyboard_manager = KeyboardManager()

    sample_query_data.current_studio = args.current_studio
    sample_query_data.studios = args.selected_studios

    # Call the function to test
    keyboard = keyboard_manager.get_locations_keyboard(sample_query_data)

    # Assert button layout rows
    assert len(keyboard.keyboard) == len(args.rows_number_of_buttons_list)
    for keyboard_list, number_of_buttons in zip(keyboard.keyboard, args.rows_number_of_buttons_list):
        assert len(keyboard_list) == number_of_buttons

    # Assert button texts and callback data
    button_texts = [button.text for row in keyboard.keyboard for button in row]
    callback_data = [button.callback_data for row in keyboard.keyboard for button in row]

    for (expected_text, expected_callback), actual_text, actual_callback in zip(
        args.expected_buttons_texts_and_callback_data, button_texts, callback_data
    ):
        assert actual_text == expected_text
        assert actual_callback == expected_callback


class GetInstructorsKeyboardArgs(NamedTuple):
    selected_studios: dict[StudioType, StudioData]
    rows_number_of_buttons_list: list[int]
    expected_buttons_texts_and_callback_data: list[tuple[str, str]]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetInstructorsKeyboardArgs(
                selected_studios={
                    StudioType.AbsoluteSpin: StudioData(),
                    StudioType.AbsolutePilates: StudioData(),
                    StudioType.AllySpin: StudioData(),
                    StudioType.AllyPilates: StudioData(),
                    StudioType.AllyRecovery: StudioData(),
                    StudioType.Anarchy: StudioData(),
                    StudioType.Barrys: StudioData(),
                    StudioType.Rev: StudioData(),
                },
                rows_number_of_buttons_list=[
                    1,  # Enter Rev Instructor(s)
                    1,  # Enter Barrys Instructor(s)
                    1,  # Enter Absolute (Spin) Instructor(s)
                    1,  # Enter Absolute (Pilates) Instructor(s)
                    1,  # Enter Ally (Spin) Instructor(s)
                    1,  # Enter Ally (Pilates) Instructor(s)
                    1,  # Enter Anarchy Instructor(s)
                    1,  # Show Names of Instructors
                    1,  # Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Enter Rev Instructor(s)", "{'step': 'rev-instructors'}"),
                    ("Enter Barrys Instructor(s)", "{'step': 'barrys-instructors'}"),
                    ("Enter Absolute (Spin) Instructor(s)", "{'step': 'absolute-spin-instructors'}"),
                    ("Enter Absolute (Pilates) Instructor(s)", "{'step': 'absolute-pilates-instructors'}"),
                    ("Enter Ally (Spin) Instructor(s)", "{'step': 'ally-spin-instructors'}"),
                    ("Enter Ally (Pilates) Instructor(s)", "{'step': 'ally-pilates-instructors'}"),
                    ("Enter Anarchy Instructor(s)", "{'step': 'anarchy-instructors'}"),
                    ("Show Names of Instructors", "{'step': 'show-instructors'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="All studios selected",
        ),
        pytest.param(
            GetInstructorsKeyboardArgs(
                selected_studios={
                    StudioType.AbsoluteSpin: StudioData(),
                    StudioType.Anarchy: StudioData(),
                    StudioType.Barrys: StudioData(),
                },
                rows_number_of_buttons_list=[
                    1,  # Enter Barrys Instructor(s)
                    1,  # Enter Absolute (Spin) Instructor(s)
                    1,  # Enter Anarchy Instructor(s)
                    1,  # Show Names of Instructors
                    1,  # Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Enter Barrys Instructor(s)", "{'step': 'barrys-instructors'}"),
                    ("Enter Absolute (Spin) Instructor(s)", "{'step': 'absolute-spin-instructors'}"),
                    ("Enter Anarchy Instructor(s)", "{'step': 'anarchy-instructors'}"),
                    ("Show Names of Instructors", "{'step': 'show-instructors'}"),
                    ("Next ▶️", "{'step': 'main-page-handler'}"),
                ],
            ),
            id="Barrys, Absolute (Spin), and Anarchy selected",
        ),
    ],
)
def test_get_instructors_keyboard(
    args: GetInstructorsKeyboardArgs,
    sample_query_data: QueryData,
) -> None:
    """
    Test the get_instructors_keyboard method to ensure the correct buttons are selected
    based on the query data.

    Args:
      - args (GetInstructorsKeyboardArgs): Provides arguments for the test case.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    keyboard_manager = KeyboardManager()

    sample_query_data.studios = args.selected_studios

    # Call the function to test
    keyboard = keyboard_manager.get_instructors_keyboard(sample_query_data)

    # Assert button layout rows
    assert len(keyboard.keyboard) == len(args.rows_number_of_buttons_list)
    for keyboard_list, number_of_buttons in zip(keyboard.keyboard, args.rows_number_of_buttons_list):
        assert len(keyboard_list) == number_of_buttons

    # Assert button texts and callback data
    button_texts = [button.text for row in keyboard.keyboard for button in row]
    callback_data = [button.callback_data for row in keyboard.keyboard for button in row]

    for (expected_text, expected_callback), actual_text, actual_callback in zip(
        args.expected_buttons_texts_and_callback_data, button_texts, callback_data
    ):
        assert actual_text == expected_text
        assert actual_callback == expected_callback


class GetDaysKeyboardArgs(NamedTuple):
    selected_days: list[str]
    rows_number_of_buttons_list: list[int]
    expected_buttons_texts_and_callback_data: list[tuple[str, str]]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetDaysKeyboardArgs(
                selected_days=["Monday", "Wednesday"],
                rows_number_of_buttons_list=[
                    2,  # Monday, Tuesday
                    2,  # Wednesday, Thursday
                    2,  # Friday, Saturday
                    1,  # Sunday
                    2,  # Select All, Unselect All
                    1,  # Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Monday ✅", "{'days': 'Monday', 'step': 'days'}"),
                    ("Tuesday", "{'days': 'Tuesday', 'step': 'days'}"),
                    ("Wednesday ✅", "{'days': 'Wednesday', 'step': 'days'}"),
                    ("Thursday", "{'days': 'Thursday', 'step': 'days'}"),
                    ("Friday", "{'days': 'Friday', 'step': 'days'}"),
                    ("Saturday", "{'days': 'Saturday', 'step': 'days'}"),
                    ("Sunday", "{'days': 'Sunday', 'step': 'days'}"),
                    ("Select All", "{'days': 'All', 'step': 'days'}"),
                    ("Unselect All", "{'days': 'None', 'step': 'days'}"),
                    ("Next ▶️", "{'step': 'days-next'}"),
                ],
            ),
            id="Monday and Wednesday selected",
        ),
        pytest.param(
            GetDaysKeyboardArgs(
                selected_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                rows_number_of_buttons_list=[
                    2,  # Monday, Tuesday
                    2,  # Wednesday, Thursday
                    2,  # Friday, Saturday
                    1,  # Sunday
                    2,  # Select All, Unselect All
                    1,  # Next
                ],
                expected_buttons_texts_and_callback_data=[
                    ("Monday ✅", "{'days': 'Monday', 'step': 'days'}"),
                    ("Tuesday ✅", "{'days': 'Tuesday', 'step': 'days'}"),
                    ("Wednesday ✅", "{'days': 'Wednesday', 'step': 'days'}"),
                    ("Thursday ✅", "{'days': 'Thursday', 'step': 'days'}"),
                    ("Friday ✅", "{'days': 'Friday', 'step': 'days'}"),
                    ("Saturday ✅", "{'days': 'Saturday', 'step': 'days'}"),
                    ("Sunday ✅", "{'days': 'Sunday', 'step': 'days'}"),
                    ("Select All", "{'days': 'All', 'step': 'days'}"),
                    ("Unselect All", "{'days': 'None', 'step': 'days'}"),
                    ("Next ▶️", "{'step': 'days-next'}"),
                ],
            ),
            id="All days selected",
        ),
    ],
)
def test_get_days_keyboard(
    args: GetDaysKeyboardArgs,
    sample_query_data: QueryData,
) -> None:
    """
    Tests that get_days_keyboard returns the correct keyboard.

    Args:
      - args (GetDaysKeyboardArgs): Provides arguments for the test case.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    keyboard_manager = KeyboardManager()

    sample_query_data.days = args.selected_days

    # Call the function to test
    keyboard = keyboard_manager.get_days_keyboard(sample_query_data)

    # Assert button layout rows
    assert len(keyboard.keyboard) == len(args.rows_number_of_buttons_list)
    for keyboard_list, number_of_buttons in zip(keyboard.keyboard, args.rows_number_of_buttons_list):
        assert len(keyboard_list) == number_of_buttons

    # Assert button texts and callback data
    button_texts = [button.text for row in keyboard.keyboard for button in row]
    callback_data = [button.callback_data for row in keyboard.keyboard for button in row]

    for (expected_text, expected_callback), actual_text, actual_callback in zip(
        args.expected_buttons_texts_and_callback_data, button_texts, callback_data
    ):
        assert actual_text == expected_text
        assert actual_callback == expected_callback


def test_get_main_page_keyboard() -> None:
    """
    Tests that get_main_page_keyboard returns the correct keyboard.
    """
    keyboard_manager = KeyboardManager()
    assert keyboard_manager.get_main_page_keyboard() == keyboard_manager.main_page_keyboard


def test_get_weeks_page_keyboard() -> None:
    """
    Tests that get_weeks_page_keyboard returns the correct keyboard.
    """
    keyboard_manager = KeyboardManager()
    assert keyboard_manager.get_weeks_page_keyboard() == keyboard_manager.weeks_page_keyboard


def test_get_timeslot_filter_keyboard() -> None:
    """
    Tests that get_timeslot_filter_keyboard returns the correct keyboard.
    """
    keyboard_manager = KeyboardManager()
    assert keyboard_manager.get_timeslot_filter_keyboard() == keyboard_manager.timeslot_filter_keyboard


def test_get_class_name_filter_keyboard() -> None:
    """
    Tests that get_class_name_filter_keyboard returns the correct keyboard.
    """
    keyboard_manager = KeyboardManager()
    assert keyboard_manager.get_class_name_filter_keyboard() == keyboard_manager.class_name_filter_keyboard
