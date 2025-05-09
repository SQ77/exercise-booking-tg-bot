"""
test_start_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the start page handler.
"""

from unittest.mock import Mock

import pytest_mock

from menu import start_page_handler


def test_start_message_handler(
    mocker: pytest_mock.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test start_message_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_time = 123.0

    # Setup mocks
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_history_manager = mocker.Mock()

    mock_time = mocker.patch("time.time")
    mock_time.return_value = test_time

    mock_main_page_handler = mocker.patch("menu.start_page_handler.main_page_handler")

    # Call the function to test
    start_page_handler.start_message_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        history_manager=mock_history_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_history_manager.add.assert_called_once_with(
        timestamp=int(test_time),
        user_id=mock_message.from_user.id,
        chat_id=mock_message.chat.id,
        username=mock_message.from_user.username,
        first_name=mock_message.from_user.first_name,
        last_name=mock_message.from_user.last_name,
        command="start",
    )

    mock_chat_manager.reset_query_and_messages_to_edit_data.assert_called_once_with(
        chat_id=mock_message.chat.id,
    )

    mock_chat_manager.add_message_id_to_delete.assert_called_once_with(
        chat_id=mock_message.chat.id,
        message_id=mock_message.id,
    )

    mock_main_page_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )
