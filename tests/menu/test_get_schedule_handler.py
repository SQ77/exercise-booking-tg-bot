"""
test_get_schedule_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the get schedule handler.
"""

from unittest.mock import Mock

import pytest_mock
import telebot

from common.query_data import QueryData
from menu.get_schedule_handler import get_schedule_callback_query_handler


def test_get_schedule_no_studio_selected(
    mocker: pytest_mock.MockerFixture,
    mock_message: Mock,
    sample_empty_query_data: QueryData,
) -> None:
    """
    Tests get_schedule_callback_query_handler when no studio is selected. Should prompt
    the user to select a studio and redirect to main page.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - sample_empty_query_data (QueryData): Sample empty QueryData object for the test.

    """

    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = sample_empty_query_data

    mock_keyboard_manager = mocker.Mock()
    mock_full_result_data = mocker.Mock()

    mock_main_page_handler = mocker.patch("menu.get_schedule_handler.main_page_handler")

    # Call the function to test
    get_schedule_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        full_result_data=mock_full_result_data,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="No studio selected. Please select a studio to get schedule for",
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )
    mock_main_page_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_get_schedule_no_day_selected(
    mocker: pytest_mock.MockerFixture,
    mock_message: Mock,
    sample_query_data: QueryData,
) -> None:
    """
    Tests get_schedule_callback_query_handler when no day is selected. Should prompt the
    user to select a day and redirect to main page.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    sample_query_data.days = []

    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = sample_query_data

    mock_keyboard_manager = mocker.Mock()
    mock_full_result_data = mocker.Mock()

    mock_main_page_handler = mocker.patch("menu.get_schedule_handler.main_page_handler")

    # Call the function to test
    get_schedule_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        full_result_data=mock_full_result_data,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="No day selected. Please select the day to get schedule for",
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )
    mock_main_page_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_get_schedule_callback_query_handler_success_results_under_4095_chars(
    mocker: pytest_mock.MockerFixture,
    mock_message: Mock,
    sample_query_data: QueryData,
) -> None:
    """
    Tests get_schedule_callback_query_handler with proper query with results under 4095
    chars. Should send the full result string to user in one message.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """
    test_result_str = "result"

    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = sample_query_data

    mock_result = mocker.Mock()
    mock_result.get_result_str.return_value = test_result_str

    mock_full_result_data = mocker.Mock()
    mock_full_result_data.get_data.return_value = mock_result

    mock_keyboard_manager = mocker.Mock()

    # Call the function to test
    get_schedule_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        full_result_data=mock_full_result_data,
    )

    # Assert that flow was called with the expected arguments
    mock_full_result_data.get_data.assert_called_once_with(query=sample_query_data)
    mock_chat_manager.reset_query_and_messages_to_edit_data.assert_called_once_with(chat_id=mock_message.chat.id)
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=test_result_str,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )


def test_get_schedule_callback_query_handler_success_results_over_4095_chars(
    mocker: pytest_mock.MockerFixture,
    mock_message: Mock,
    sample_query_data: QueryData,
) -> None:
    """
    Tests get_schedule_callback_query_handler with proper query with results over 4095
    chars. Should split and send multiple messages.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - sample_query_data (QueryData): Sample QueryData object for the test.

    """

    total_lines = 500
    lines_list = ["test_line"] * total_lines
    test_result_str = "\n".join(lines_list)

    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = sample_query_data

    mock_result = mocker.Mock()
    mock_result.get_result_str.return_value = test_result_str

    mock_full_result_data = mocker.Mock()
    mock_full_result_data.get_data.return_value = mock_result

    mock_keyboard_manager = mocker.Mock()

    # Call the function to test
    get_schedule_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        full_result_data=mock_full_result_data,
    )

    # Assert that flow was called with the expected arguments
    mock_full_result_data.get_data.assert_called_once_with(query=sample_query_data)
    mock_chat_manager.reset_query_and_messages_to_edit_data.assert_called_once_with(chat_id=mock_message.chat.id)

    first_call_lines = 409  # 4090 characters. Each line is appended with a newline
    expected_first_call_lines = ["test_line"] * first_call_lines
    expected_first_call_str = "\n".join(expected_first_call_lines) + "\n"
    expected_second_call_lines = ["test_line"] * (total_lines - first_call_lines)  # Remaining 91 lines.
    expected_second_call_str = "\n".join(expected_second_call_lines) + "\n"
    expected_send_prompt_calls = [
        mocker.call(
            chat_id=mock_message.chat.id,
            text=expected_first_call_str,
            reply_markup=None,
            delete_sent_msg_in_future=False,
        ),
        mocker.call(
            chat_id=mock_message.chat.id,
            text=expected_second_call_str,
            reply_markup=None,
            delete_sent_msg_in_future=False,
        ),
    ]
    assert mock_chat_manager.send_prompt.call_args_list == expected_send_prompt_calls
