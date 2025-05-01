"""
test_weeks_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the weeks page handler.
"""

from unittest.mock import Mock

import pytest_mock

from menu import weeks_page_handler


def test_weeks_selection_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test weeks_selection_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_query_str = "test query str"

    # Setup mocks
    mock_query_data = mocker.Mock()
    mock_query_data.get_query_str.return_value = test_query_str

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_weeks_page_keyboard = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_keyboard_manager.get_weeks_page_keyboard.return_value = mock_weeks_page_keyboard

    mock_query = mocker.Mock()

    # Call the function to test
    weeks_page_handler.weeks_selection_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.get_query_data.assert_called_once_with(chat_id=mock_query.message.chat.id)
    mock_query_data.get_query_str.assert_called_once_with(include_weeks=True)
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_query.message.chat.id,
        text=(
            "*Currently selected week(s)*\n"
            f"{test_query_str}"
            "\nAbsolute shows up to 1.5 weeks\nAlly shows up to 2 weeks\n"
            "Anarchy shows up to 2.5 weeks\nBarrys shows up to 3 weeks\nRev shows up to 4 weeks\n"
        ),
        reply_markup=mock_weeks_page_keyboard,
        delete_sent_msg_in_future=True,
    )


def test_weeks_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test weeks_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_weeks = 3

    # Setup mocks
    mock_main_page_handler = mocker.patch("menu.weeks_page_handler.main_page_handler")
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    mock_query = mocker.Mock()
    mock_query.data = str({"weeks": test_weeks})

    # Call the function to test
    weeks_page_handler.weeks_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.update_query_data_weeks.assert_called_once_with(
        chat_id=mock_query.message.chat.id,
        weeks=test_weeks,
    )
    mock_main_page_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )
