"""
test_days_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the days page handler.
"""
import menu.days_page_handler as days_page_handler
import pytest
import telebot
from common.data import SORTED_DAYS
from typing import NamedTuple

class DaysPageCallbackQueryHandlerArgs(NamedTuple):
  query_data_days: list[str]
  selected_day: str
  expected_updated_days: list[str]
  expected_query_str: str

@pytest.mark.parametrize(
  "args",
  [
    pytest.param(
      DaysPageCallbackQueryHandlerArgs(
        query_data_days=["Monday", "Tuesday"],
        selected_day="Tuesday",
        expected_updated_days=["Monday"],
        expected_query_str="Mock Query String"
      ),
      id="Unselect existing day"
    ),
    pytest.param(
      DaysPageCallbackQueryHandlerArgs(
        query_data_days=["Monday"],
        selected_day="Tuesday",
        expected_updated_days=["Monday", "Tuesday"],
        expected_query_str="Mock Query String"
      ),
      id="Select new day"
    ),
    pytest.param(
      DaysPageCallbackQueryHandlerArgs(
        query_data_days=["Monday", "Tuesday"],
        selected_day="None",
        expected_updated_days=[],
        expected_query_str="No days selected"
      ),
      id="Reset all days"
    ),
    pytest.param(
      DaysPageCallbackQueryHandlerArgs(
        query_data_days=[],
        selected_day="All",
        expected_updated_days=SORTED_DAYS,
        expected_query_str="All days selected"
      ),
      id="Select all days"
    ),
  ]
)
def test_days_page_callback_query_handler(mocker, args):
  """
  Parametrized test for days_page_callback_query_handler.

  Args:
    - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
    - args (DaysPageCallbackQueryHandlerArgs): Provides arguments for the test case.
  """
  test_chat_id = 123
  test_message_id = 456

  # Setup mocks
  mock_chat = mocker.Mock(id=test_chat_id)
  mock_message = mocker.Mock(spec=telebot.types.Message, chat=mock_chat)

  mock_query = mocker.Mock(spec=telebot.types.CallbackQuery)
  mock_query.message = mock_message
  mock_query.data = str({"days": args.selected_day})

  query_data_mock = mocker.Mock()
  query_data_mock.days = args.query_data_days
  query_data_mock.get_query_str.return_value = args.expected_query_str

  mock_chat_manager = mocker.Mock()
  mock_chat_manager.get_query_data.return_value = query_data_mock
  mock_chat_manager.get_days_selection_message.return_value = mocker.Mock(
    chat=mocker.Mock(id=test_chat_id),
    id=test_message_id,
  )

  mock_keyboard_manager = mocker.Mock()
  mock_keyboard_manager.get_days_keyboard.return_value = "Mock Keyboard"
  mock_bot = mocker.Mock()

  # Call the function to test
  days_page_handler.days_page_callback_query_handler(
    query=mock_query,
    bot=mock_bot,
    chat_manager=mock_chat_manager,
    keyboard_manager=mock_keyboard_manager,
  )

  # Assert that flow was called with the expected arguments
  mock_chat_manager.update_query_data_days.assert_any_call(
    chat_id=test_chat_id,
    days=args.expected_updated_days,
  )

  mock_bot.edit_message_text.assert_called_once_with(
    chat_id=test_chat_id,
    message_id=test_message_id,
    text=f"*Currently selected day(s)*\n{args.expected_query_str}",
    reply_markup="Mock Keyboard",
    parse_mode="Markdown",
  )

  # Assert that global variables was not modified
  assert SORTED_DAYS == ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
