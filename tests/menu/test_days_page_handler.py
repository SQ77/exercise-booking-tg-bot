"""
test_days_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the days page handler.
"""

from typing import NamedTuple

import pytest
import pytest_mock
import telebot

import menu.days_page_handler as days_page_handler
from common.data import SORTED_DAYS


class DaysPageCallbackQueryHandlerArgs(NamedTuple):
    initial_days: list[str]
    selected_days_sequence: list[str]
    expected_updated_days_sequence: list[list[str]]
    expected_query_str: str


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["All", "Thursday", "Friday", "Friday"],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday", "Sunday"],
                    ["Monday", "Tuesday", "Wednesday", "Saturday", "Sunday"],
                    ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday", "Sunday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="All -> Unselect Thursday -> Unselect Friday -> Select Friday",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["All", "None", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    [],
                    ["Monday"],
                    ["Monday", "Tuesday"],
                    ["Monday", "Tuesday", "Wednesday"],
                    ["Monday", "Tuesday", "Wednesday", "Thursday"],
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id=(
                "Select All -> Reset -> Select Monday -> Select Tuesday -> "
                "Select Wednesday -> Select Thursday -> Select Friday"
            ),
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["Monday", "Monday", "Monday"],
                expected_updated_days_sequence=[
                    ["Monday"],
                    [],
                    ["Monday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select Monday -> Unselect Monday -> Select Monday",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=["Monday", "Tuesday"],
                selected_days_sequence=["All"],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Start with some days -> Select All",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["Tuesday", "Thursday", "Tuesday", "All"],
                expected_updated_days_sequence=[
                    ["Tuesday"],
                    ["Tuesday", "Thursday"],
                    ["Thursday"],
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select Tuesday -> Select Thursday -> Unselect Tuesday -> Select All",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["All", "None", "Saturday", "Sunday"],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    [],
                    ["Saturday"],
                    ["Saturday", "Sunday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select All -> Reset -> Select Saturday -> Select Sunday",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=[
                    "All",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Thursday", "Friday", "Saturday", "Sunday"],
                    ["Friday", "Saturday", "Sunday"],
                    ["Saturday", "Sunday"],
                    ["Sunday"],
                    [],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select All -> Unselect each day one by one",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=["Monday", "Tuesday"],
                selected_days_sequence=["None", "None", "None"],
                expected_updated_days_sequence=[
                    [],
                    [],
                    [],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Reset repeatedly",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["All", "All", "All"],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select All repeatedly",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["Friday", "Friday", "Friday", "Friday", "Friday", "Friday"],
                expected_updated_days_sequence=[
                    ["Friday"],
                    [],
                    ["Friday"],
                    [],
                    ["Friday"],
                    [],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Stress test for single day",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["All", "None", "All"],
                expected_updated_days_sequence=[
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    [],
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select All -> Reset -> Select All",
        ),
        pytest.param(
            DaysPageCallbackQueryHandlerArgs(
                initial_days=[],
                selected_days_sequence=["Friday", "Monday", "Wednesday"],
                expected_updated_days_sequence=[
                    ["Friday"],
                    ["Monday", "Friday"],
                    ["Monday", "Wednesday", "Friday"],
                ],
                expected_query_str="Mock Query String",
            ),
            id="Select days out of order",
        ),
    ],
)
def test_days_page_callback_query_handler_multi_step(
    mocker: pytest_mock.plugin.MockerFixture,
    args: DaysPageCallbackQueryHandlerArgs,
) -> None:
    """
    Parametrized test for days_page_callback_query_handler. Multi-step test to simulate
    a user pressing buttons in a selected_days_sequence.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (DaysPageCallbackQueryHandlerArgs): Provides arguments for the test case.

    """
    assert len(args.selected_days_sequence) == len(args.expected_updated_days_sequence), (
        f"Invalid arguments in test case: "
        f"selected_days_sequence has {len(args.selected_days_sequence)} items but "
        f"expected_updated_days_sequence has {len(args.expected_updated_days_sequence)} items. "
        "Each selected day must have a corresponding expected update."
    )

    test_chat_id = 123
    test_message_id = 456

    # Setup mocks
    mock_chat = mocker.Mock(id=test_chat_id)
    mock_message = mocker.Mock(spec=telebot.types.Message, chat=mock_chat)

    query_data_mock = mocker.Mock()
    query_data_mock.days = args.initial_days.copy()
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

    # Run through the sequence of button presses
    for index, selected_day in enumerate(args.selected_days_sequence):
        mock_query = mocker.Mock(spec=telebot.types.CallbackQuery)
        mock_query.message = mock_message
        mock_query.data = str({"days": selected_day})

        # Run handler for each button press
        days_page_handler.days_page_callback_query_handler(
            query=mock_query,
            bot=mock_bot,
            chat_manager=mock_chat_manager,
            keyboard_manager=mock_keyboard_manager,
        )

        # Assert that flow was called with the expected arguments
        mock_bot.edit_message_text.assert_called_with(
            chat_id=test_chat_id,
            message_id=test_message_id,
            text=f"*Currently selected day(s)*\n{args.expected_query_str}",
            reply_markup="Mock Keyboard",
            parse_mode="Markdown",
        )

        mock_chat_manager.update_query_data_days.assert_called_with(
            chat_id=test_chat_id,
            days=args.expected_updated_days_sequence[index],
        )

        # Update return value of get_query_data for the next call
        query_data_mock.days = args.expected_updated_days_sequence[index]

    # Double check global state is untouched
    assert SORTED_DAYS == ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
