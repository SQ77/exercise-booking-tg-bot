"""
test_name_filter_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the name filter page handler.
"""

from unittest.mock import Mock

import pytest_mock
import telebot

from menu import name_filter_page_handler


def test_class_name_filter_selection_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
) -> None:
    """
    Test class_name_filter_selection_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_class_name_filter_selection_handler = mocker.patch(
        "menu.name_filter_page_handler.class_name_filter_selection_handler",
    )
    mock_query = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    # Call the function to test
    name_filter_page_handler.class_name_filter_selection_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_class_name_filter_selection_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_class_name_filter_selection_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test class_name_filter_selection_handler flow.

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

    mock_class_name_filter_keyboard = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_keyboard_manager.get_class_name_filter_keyboard.return_value = mock_class_name_filter_keyboard

    # Call the function to test
    name_filter_page_handler.class_name_filter_selection_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=f"*Current filter*\n{test_query_str}",
        reply_markup=mock_class_name_filter_keyboard,
        delete_sent_msg_in_future=True,
    )


def test_class_name_filter_set_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test class_name_filter_set_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_query_str = "test query str"

    # Setup mocks
    mock_query_data = mocker.Mock()
    mock_query_data.get_query_str.return_value = test_query_str

    mock_sent_msg = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    mock_bot = mocker.Mock()
    mock_query = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    # Call the function to test
    name_filter_page_handler.class_name_filter_set_callback_query_handler(
        query=mock_query,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_query.message.chat.id,
        text="Enter name of class to filter (non-case sensitive)\ne.g. *essential*",
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )
    mock_bot.register_next_step_handler.assert_called_once_with(
        message=mock_sent_msg,
        callback=name_filter_page_handler.class_name_filter_input_handler,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_class_name_filter_input_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test class_name_filter_input_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_text = "test filter"

    # Setup mocks
    mock_class_name_filter_selection_handler = mocker.patch(
        "menu.name_filter_page_handler.class_name_filter_selection_handler",
    )
    mock_query_data = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data
    mock_keyboard_manager = mocker.Mock()
    mock_message.text = test_text

    # Call the function to test
    name_filter_page_handler.class_name_filter_input_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.get_query_data.assert_called_once_with(chat_id=mock_message.chat.id)
    mock_class_name_filter_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that the response is as expected
    assert mock_query_data.class_name_filter == test_text


def test_class_name_filter_reset_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test class_name_filter_reset_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_class_name_filter_selection_handler = mocker.patch(
        "menu.name_filter_page_handler.class_name_filter_selection_handler",
    )
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)
    mock_query_data = mocker.Mock()
    mock_query_data.class_name_filter = "test filter"
    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data
    mock_keyboard_manager = mocker.Mock()

    # Call the function to test
    name_filter_page_handler.class_name_filter_reset_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.get_query_data.assert_called_once_with(chat_id=mock_message.chat.id)
    mock_class_name_filter_selection_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that the response is as expected
    assert mock_query_data.class_name_filter == ""
