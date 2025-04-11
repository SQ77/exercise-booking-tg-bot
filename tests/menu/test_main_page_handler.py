"""
test_main_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the main page handler.
"""

import pytest_mock
import telebot

import menu.main_page_handler as main_page_handler


def test_main_page_handler(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test main_page_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    test_chat_id = 123
    test_get_query_str = "Mock Query String"
    test_main_page_keyboard = "Mock Keyboard"

    mock_chat = mocker.Mock()
    mock_chat.id = test_chat_id

    mock_message = mocker.Mock(spec=telebot.types.Message)
    mock_message.chat = mock_chat

    mock_query_data = mocker.Mock()
    mock_query_data.get_query_str.return_value = test_get_query_str

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_keyboard_manager = mocker.Mock()
    mock_keyboard_manager.get_main_page_keyboard.return_value = test_main_page_keyboard

    # Call the function to test
    main_page_handler.main_page_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.get_query_data.assert_called_once_with(chat_id=test_chat_id)
    mock_query_data.get_query_str.assert_called_once_with(
        include_studio=True,
        include_instructors=True,
        include_weeks=True,
        include_days=True,
        include_time=True,
        include_class_name_filter=True,
    )
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=test_chat_id,
        text=f"*Schedule to check*\n{test_get_query_str}",
        reply_markup=test_main_page_keyboard,
        delete_sent_msg_in_future=True,
    )
    mock_keyboard_manager.get_main_page_keyboard.assert_called_once()


def test_main_page_callback_query_handler(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test main_page_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    test_chat_id = 123
    test_get_query_str = "Mock Query String"
    test_main_page_keyboard = "Mock Keyboard"

    mock_chat = mocker.Mock()
    mock_chat.id = test_chat_id

    mock_message = mocker.Mock(spec=telebot.types.Message)
    mock_message.chat = mock_chat

    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery)
    mock_query.message = mock_message

    mock_query_data = mocker.Mock()
    mock_query_data.get_query_str.return_value = test_get_query_str

    mock_chat_manager = mocker.Mock()
    mock_chat_manager.get_query_data.return_value = mock_query_data

    mock_keyboard_manager = mocker.Mock()
    mock_keyboard_manager.get_main_page_keyboard.return_value = test_main_page_keyboard

    # Spy on main_page_handler
    spy = mocker.spy(main_page_handler, "main_page_handler")

    # Call the function to test
    main_page_handler.main_page_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that the internal main_page_handler was called with the expected arguments
    spy.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )
