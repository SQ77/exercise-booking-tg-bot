"""
test_time_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the time page handler.
"""

from copy import copy
from datetime import date, datetime
from typing import NamedTuple
from unittest.mock import Mock

import pytest
import pytest_mock
import telebot

import menu.time_page_handler as time_page_handler
from common.query_data import QueryData


def test_time_selection_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_time_selection_handler = mocker.patch("menu.time_page_handler.time_selection_handler")

    # Call the function to test
    time_page_handler.time_selection_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_time_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_time_selection_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    test_get_query_str = "Mock Query String"

    mock_query_data = mocker.Mock(spec=QueryData)
    mock_query_data.get_query_str.return_value = test_get_query_str

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_timeslot_filter_keyboard = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_keyboard_manager.get_timeslot_filter_keyboard.return_value = mock_timeslot_filter_keyboard

    # Call the function to test
    time_page_handler.time_selection_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.get_query_data.assert_called_once_with(chat_id=mock_message.chat.id)
    mock_query_data.get_query_str.assert_called_once_with(include_time=True)
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=f"*Currently selected timings(s)*\n{test_get_query_str}",
        reply_markup=mock_timeslot_filter_keyboard,
        delete_sent_msg_in_future=True,
    )


def test_time_selection_add_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_add_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    mock_start_time_selection_handler = mocker.patch("menu.time_page_handler.start_time_selection_handler")

    # Call the function to test
    time_page_handler.time_selection_add_callback_query_handler(
        query=mock_query,
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_start_time_selection_handler.assert_called_once_with(
        message=mock_message,
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_start_time_selection_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test start_time_selection_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    # Call the function to test
    time_page_handler.start_time_selection_handler(
        message=mock_message,
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="Enter range of timeslot to check\ne.g. *0700-0830*",
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    mock_bot.register_next_step_handler.assert_called_once_with(
        message=mock_sent_msg,
        callback=time_page_handler.timeslot_input_handler,
        logger=mock_logger,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


class TimeslotInputHandlerFailureArgs(NamedTuple):
    message_text: str
    expected_error_text: str
    current_timeslots: list[tuple[date, date]] = []


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="2359",
                expected_error_text="Invalid timeslot range '2359' entered",
            ),
            id="Invalid timeslot - Not valid range",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="12345-2359",
                expected_error_text="Invalid timeslot range '12345-2359' entered",
            ),
            id="Invalid timeslot - Invalid start time length",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="0000-50000",
                expected_error_text="Invalid timeslot range '0000-50000' entered",
            ),
            id="Invalid timeslot - Invalid end time length",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="1600-1330",
                expected_error_text="End time must be later than or equal start time. Start time: 1600, End time: 1330",
            ),
            id="Invalid timeslot - End time earlier than start time",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="0830-1100",
                expected_error_text="Start time '0830' conflicts with existing timeslot '0800 - 1000'",
                current_timeslots=[(datetime.strptime("0800", "%H%M"), datetime.strptime("1000", "%H%M"))],
            ),
            id="Invalid timeslot - Start time falls within existing timeslot",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="0800-0800",
                expected_error_text="Start time '0800' conflicts with existing timeslot '0800 - 0800'",
                current_timeslots=[(datetime.strptime("0800", "%H%M"), datetime.strptime("0800", "%H%M"))],
            ),
            id="Invalid timeslot - Duplicate timeslots",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="0700-0830",
                expected_error_text="End time '0830' conflicts with existing timeslot '0800 - 0900'",
                current_timeslots=[(datetime.strptime("0800", "%H%M"), datetime.strptime("0900", "%H%M"))],
            ),
            id="Invalid timeslot - End time falls within existing timeslot",
        ),
        pytest.param(
            TimeslotInputHandlerFailureArgs(
                message_text="0700-0930",
                expected_error_text="Time range '0700 - 0930' conflicts with existing timeslot '0800 - 0900'",
                current_timeslots=[(datetime.strptime("0800", "%H%M"), datetime.strptime("0900", "%H%M"))],
            ),
            id="Invalid timeslot - Timeslot contains existing timeslot",
        ),
    ],
)
def test_timeslot_input_handler_failures(
    mocker: pytest_mock.plugin.MockerFixture,
    args: TimeslotInputHandlerFailureArgs,
    mock_message: Mock,
    sample_query_data: QueryData,
) -> None:
    """
    Test timeslot_input_handler failure flows.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (TimeslotInputHandlerFailureArgs): Provides arguments for the test case.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    # Setup mocks
    mock_message.text = args.message_text

    mock_logger = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    sample_query_data.start_times = args.current_timeslots
    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = sample_query_data

    mock_time_selection_handler = mocker.patch("menu.time_page_handler.time_selection_handler")

    # Call the function to test
    time_page_handler.timeslot_input_handler(
        message=mock_message,
        logger=mock_logger,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=args.expected_error_text,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )

    mock_time_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_timeslot_input_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test timeslot_input_handler success flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    timeslots_to_add = [
        ("1100", "1400"),
        ("0700", "0900"),
        ("1700", "2359"),
    ]

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    mock_query_data = mocker.Mock(start_times=[])

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    expected_timeslots = []
    for index, (start_time_str, end_time_str) in enumerate(timeslots_to_add):
        mock_message.text = f"{start_time_str}-{end_time_str}"
        mock_time_selection_handler = mocker.patch("menu.time_page_handler.time_selection_handler")

        # Call the function to test
        time_page_handler.timeslot_input_handler(
            message=mock_message,
            logger=mock_logger,
            chat_manager=mock_chat_manager,
            keyboard_manager=mock_keyboard_manager,
        )

        # Assert that flow was called with the expected arguments
        mock_time_selection_handler.assert_called_once_with(
            message=mock_message,
            chat_manager=mock_chat_manager,
            keyboard_manager=mock_keyboard_manager,
        )

        start_time = datetime.strptime(start_time_str, "%H%M")
        end_time = datetime.strptime(end_time_str, "%H%M")
        expected_timeslots.append((start_time, end_time))
        expected_timeslots = sorted(expected_timeslots)
        assert len(mock_query_data.start_times) == index + 1
        assert mock_query_data.start_times == expected_timeslots


def test_time_selection_remove_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_remove_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_time_selection_remove_handler = mocker.patch("menu.time_page_handler.time_selection_remove_handler")

    # Call the function to test
    time_page_handler.time_selection_remove_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_time_selection_remove_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_time_selection_remove_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_remove_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_start_time_str = "0800"
    test_end_time_str = "1000"
    expected_keyboard = telebot.types.InlineKeyboardMarkup()
    expected_keyboard.add(
        telebot.types.InlineKeyboardButton(
            text=f"{test_start_time_str} - {test_end_time_str}",
            callback_data=str(
                f"{{'step': 'remove-timeslot', 'start':'{test_start_time_str}', " f"'end':'{test_end_time_str}'}}"
            ),
        )
    )
    expected_keyboard.add(
        telebot.types.InlineKeyboardButton(
            text="◀️ Back",
            callback_data="{'step': 'time-selection'}",
        )
    )

    # Setup mocks
    mock_query_data = mocker.Mock(
        start_times=[(datetime.strptime(test_start_time_str, "%H%M"), datetime.strptime(test_end_time_str, "%H%M"))]
    )

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_keyboard_manager = mocker.Mock()

    # Call the function to test
    time_page_handler.time_selection_remove_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that the response is as expected
    assert mock_chat_manager.send_prompt.call_count == 1

    actual_args, actual_kwargs = mock_chat_manager.send_prompt.call_args
    assert actual_kwargs["chat_id"] == mock_message.chat.id
    assert actual_kwargs["text"] == "*Select timeslot to remove*"
    assert actual_kwargs["delete_sent_msg_in_future"] is True
    assert actual_kwargs["reply_markup"] is not None
    assert actual_kwargs["reply_markup"].row_width == expected_keyboard.row_width

    actual_keyboard_list = actual_kwargs["reply_markup"].keyboard
    assert len(actual_keyboard_list) == len(expected_keyboard.keyboard)

    for actual_button_list, expected_button_list in zip(actual_keyboard_list, expected_keyboard.keyboard):
        assert len(actual_button_list) == len(expected_button_list)
        for actual_button, expected_button in zip(actual_button_list, expected_button_list):
            assert actual_button.text == expected_button.text
            assert actual_button.callback_data == expected_button.callback_data


def test_time_selection_remove_handler_no_timeslots(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_remove_handler no timeslots to remove flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks

    mock_query_data = mocker.Mock(start_times=[])

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_keyboard_manager = mocker.Mock()

    mock_time_selection_handler = mocker.patch("menu.time_page_handler.time_selection_handler")

    # Call the function to test
    time_page_handler.time_selection_remove_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="No timeslot to remove",
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )

    mock_time_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_time_selection_remove_timeslot_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_remove_timeslot_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    timeslots = [
        ("1100", "1400"),
        ("0000", "0900"),
        ("1700", "2359"),
    ]
    expected_start_times = [
        (datetime.strptime("0000", "%H%M"), datetime.strptime("0900", "%H%M")),
        (datetime.strptime("1100", "%H%M"), datetime.strptime("1400", "%H%M")),
        (datetime.strptime("1700", "%H%M"), datetime.strptime("2359", "%H%M")),
    ]

    # Setup mocks
    mock_query_data = mocker.Mock(start_times=copy(expected_start_times))

    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_keyboard_manager = mocker.Mock()

    for start_time_str, end_time_str in timeslots:
        mock_query.data = str({"start": f"{start_time_str}", "end": f"{end_time_str}"})

        mock_time_selection_handler = mocker.patch("menu.time_page_handler.time_selection_handler")

        # Call the function to test
        time_page_handler.time_selection_remove_timeslot_callback_query_handler(
            query=mock_query,
            chat_manager=mock_chat_manager,
            keyboard_manager=mock_keyboard_manager,
        )

        # Assert that flow was called with the expected arguments
        mock_time_selection_handler.assert_called_once_with(
            message=mock_message,
            chat_manager=mock_chat_manager,
            keyboard_manager=mock_keyboard_manager,
        )

        # Assert that the response is as expected
        expected_start_times.remove(
            (datetime.strptime(start_time_str, "%H%M"), datetime.strptime(end_time_str, "%H%M"))
        )

        assert mock_query_data.start_times == expected_start_times


def test_time_selection_reset_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test time_selection_reset_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_query_data = mocker.Mock(
        start_times=[
            (datetime.strptime("0000", "%H%M"), datetime.strptime("0900", "%H%M")),
            (datetime.strptime("1100", "%H%M"), datetime.strptime("1400", "%H%M")),
            (datetime.strptime("1700", "%H%M"), datetime.strptime("2359", "%H%M")),
        ],
    )

    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_keyboard_manager = mocker.Mock()

    mock_time_selection_handler = mocker.patch("menu.time_page_handler.time_selection_handler")

    # Call the function to test
    time_page_handler.time_selection_reset_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_time_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that the response is as expected
    assert len(mock_query_data.start_times) == 0
