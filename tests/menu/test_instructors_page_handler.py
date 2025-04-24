"""
test_instructors_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the instructors page handler.
"""

from copy import copy
from typing import NamedTuple, Protocol
from unittest.mock import Mock

import pytest
import pytest_mock
import telebot

import menu.instructors_page_handler as instructors_page_handler
from chat.chat_manager import ChatManager
from chat.keyboard_manager import KeyboardManager
from common.query_data import QueryData
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


def test_instructors_message_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test instructors_message_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """
    test_time = 123.0

    # Setup mocks
    mock_chat_manager = mocker.Mock()
    mock_history_manager = mocker.Mock()

    mock_time = mocker.patch("time.time", return_value=mocker.MagicMock(spec=float))
    mock_time.return_value = test_time

    # Call the function to test
    instructors_page_handler.instructors_message_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        history_manager=mock_history_manager,
        studios_manager=mock_studios_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_history_manager.add.assert_called_once_with(
        timestamp=int(test_time),
        user_id=mock_message.from_user.id,
        chat_id=mock_message.chat.id,
        username=mock_message.from_user.username,
        first_name=mock_message.from_user.first_name,
        last_name=mock_message.from_user.last_name,
        command="instructors",
    )

    mock_chat_manager.add_message_id_to_delete.assert_called_once_with(
        chat_id=mock_message.chat.id,
        message_id=mock_message.id,
    )

    expected_text = (
        "*Rev Instructors:* rev instructor a, rev instructor b\n\n"
        "*Barrys Instructors:* barrys instructor a, barrys instructor b\n\n"
        "*Absolute Instructors:* absolute instructor a, absolute instructor b\n\n"
        "*Ally Instructors:* ally instructor a, ally instructor b\n\n"
        "*Anarchy Instructors:* anarchy instructor a, anarchy instructor b\n\n"
    )
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=expected_text,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )


def test_instructors_selection_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test instructors_selection_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()

    mock_instructors_selection_handler = mocker.patch("menu.instructors_page_handler.instructors_selection_handler")

    # Call the function to test
    instructors_page_handler.instructors_selection_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_instructors_selection_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_show_instructors_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test show_instructors_callback_query_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """
    test_studios = {
        StudioType.AbsoluteSpin: StudioData(
            locations=[StudioLocation.Orchard, StudioLocation.Raffles],
            instructors=["Absolute Instructor", "Spin Instructor"],
        ),
        StudioType.AllyPilates: StudioData(
            locations=[StudioLocation.CrossStreet],
            instructors=["Ally Instructor", "Reformer Instructor"],
        ),
        StudioType.AllyRecovery: StudioData(locations=[StudioLocation.CrossStreet]),
        StudioType.Anarchy: StudioData(
            locations=[StudioLocation.Robinson],
            instructors=["Anarchy Instructor"],
        ),
        StudioType.Barrys: StudioData(
            locations=[StudioLocation.Orchard, StudioLocation.Raffles],
            instructors=["Barrys Instructor"],
        ),
        StudioType.Rev: StudioData(locations=[StudioLocation.Bugis], instructors=["Rev Instructor"]),
    }

    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.get_query_data.return_value = QueryData(
        studios=test_studios,
        current_studio=StudioType.AbsoluteSpin,
        weeks=3,
        days=["Monday", "Wednesday", "Friday"],
        start_times=[],
        class_name_filter="",
    )

    mock_keyboard_manager = mocker.Mock()

    mock_instructors_selection_handler = mocker.patch("menu.instructors_page_handler.instructors_selection_handler")

    # Call the function to test
    instructors_page_handler.show_instructors_callback_query_handler(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        studios_manager=mock_studios_manager,
    )

    # Assert that flow was called with the expected arguments
    expected_text = (
        "*Rev Instructors:* rev instructor a, rev instructor b\n\n"
        "*Barrys Instructors:* barrys instructor a, barrys instructor b\n\n"
        "*Absolute Instructors:* absolute instructor a, absolute instructor b\n\n"
        "*Ally Instructors:* ally instructor a, ally instructor b\n\n"
        "No instructors for Ally (Recovery)\n\n"
        "*Anarchy Instructors:* anarchy instructor a, anarchy instructor b\n\n"
    )
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=expected_text,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )

    mock_instructors_selection_handler.assert_called_once_with(
        message=mock_query.message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


class StudioInstructorsCallbackQueryHandlerFunc(Protocol):
    def __call__(
        self,
        query: telebot.types.CallbackQuery,
        chat_manager: ChatManager,
        keyboard_manager: KeyboardManager,
        bot: telebot.TeleBot,
        instructorid_map: dict[str, str],
    ) -> None: ...


class StudioInstructorsCallbackQueryHandlerArgs(NamedTuple):
    function_to_test: StudioInstructorsCallbackQueryHandlerFunc
    expected_text: str
    expected_current_studio: StudioType


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.rev_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\ne.g.: *chloe*, *jerlyn*, *zai*\n"
                    "Enter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.Rev,
            ),
            id="Rev",
        ),
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.barrys_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\ne.g.: *ria*, *gino*\n"
                    "Enter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.Barrys,
            ),
            id="Barrys",
        ),
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.absolute_spin_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\ne.g.: *chin*, *ria*\n"
                    "Enter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.AbsoluteSpin,
            ),
            id="Absolute (Spin)",
        ),
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.absolute_pilates_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\n"
                    "e.g.: *daniella*, *vnex*\nEnter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.AbsolutePilates,
            ),
            id="Absolute (Pilates)",
        ),
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.ally_spin_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\n"
                    "e.g.: *samuel*, *jasper*\nEnter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.AllySpin,
            ),
            id="Ally (Spin)",
        ),
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.ally_pilates_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\n"
                    "e.g.: *candice*, *ruth*\nEnter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.AllyPilates,
            ),
            id="Ally (Pilates)",
        ),
        pytest.param(
            StudioInstructorsCallbackQueryHandlerArgs(
                function_to_test=instructors_page_handler.anarchy_instructors_callback_query_handler,
                expected_text=(
                    "Enter instructor names separated by a comma\n"
                    "e.g.: *lyon*, *isabelle*\nEnter '*all*' to check for all instructors"
                ),
                expected_current_studio=StudioType.Anarchy,
            ),
            id="Anarchy",
        ),
    ],
)
def test_studio_instructors_callback_query_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    args: StudioInstructorsCallbackQueryHandlerArgs,
    mock_message: Mock,
) -> None:
    """
    Parametrized test for *_instructors_callback_query_handler.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (StudioInstructorsCallbackQueryHandlerArgs): Provides arguments for the test case.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_instructorid_map = {"1": "2", "3": "4", "5": "6"}

    # Setup mocks
    mock_query = mocker.Mock(spec=telebot.types.CallbackQuery, message=mock_message)

    mock_sent_msg = mocker.Mock()
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    mock_keyboard_manager = mocker.Mock()
    mock_bot = mocker.Mock()

    # Call the function to test
    args.function_to_test(
        query=mock_query,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        bot=mock_bot,
        instructorid_map=test_instructorid_map,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.update_query_data_current_studio.assert_called_once_with(
        chat_id=mock_message.chat.id,
        current_studio=args.expected_current_studio,
    )

    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=args.expected_text,
        reply_markup=None,
        delete_sent_msg_in_future=True,
    )

    mock_bot.register_next_step_handler.assert_called_once_with(
        message=mock_sent_msg,
        callback=instructors_page_handler.instructors_input_handler,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        instructorid_map=test_instructorid_map,
    )


def test_instructors_input_handler_all_flow(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test instructors_input_handler "all" instructors selected flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_instructorid_map = {"1": "2", "3": "4", "5": "6"}
    test_studios = {
        StudioType.AbsoluteSpin: StudioData(
            locations=[StudioLocation.Raffles],
            instructors=[],
        )
    }
    test_query_data = QueryData(
        studios=test_studios,
        current_studio=StudioType.AbsoluteSpin,
        weeks=3,
        days=["Monday", "Wednesday", "Friday"],
        start_times=[],
        class_name_filter="",
    )

    expected_updated_studios = copy(test_studios)
    expected_updated_studios[StudioType.AbsoluteSpin].instructors = ["All"]

    # Setup mocks
    mock_message.text = "all"

    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.get_query_data.return_value = test_query_data

    mock_keyboard_manager = mocker.Mock()

    mock_instructors_selection_handler = mocker.patch("menu.instructors_page_handler.instructors_selection_handler")

    # Call the function to test
    instructors_page_handler.instructors_input_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        instructorid_map=test_instructorid_map,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.update_query_data_studios.assert_called_once_with(
        chat_id=mock_message.chat.id,
        studios=expected_updated_studios,
    )

    mock_instructors_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_instructors_input_handler_invalid_instructors_flow(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test instructors_input_handler invalid instructors selected flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_instructorid_map = {"anarchy instructor": "1"}
    test_studios = {
        StudioType.Anarchy: StudioData(
            locations=[StudioLocation.Robinson],
            instructors=[],
        )
    }
    test_query_data = QueryData(
        studios=test_studios,
        current_studio=StudioType.Anarchy,
        weeks=3,
        days=["Monday", "Wednesday", "Friday"],
        start_times=[],
        class_name_filter="",
    )

    expected_updated_studios = copy(test_studios)
    expected_updated_studios[StudioType.Anarchy].instructors = ["anarchy instructor"]

    # Setup mocks
    mock_message.text = "/, Anarchy Instructor, Unknown"

    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.get_query_data.return_value = test_query_data

    mock_keyboard_manager = mocker.Mock()

    mock_instructors_selection_handler = mocker.patch("menu.instructors_page_handler.instructors_selection_handler")

    # Call the function to test
    instructors_page_handler.instructors_input_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        instructorid_map=test_instructorid_map,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.update_query_data_studios.assert_called_once_with(
        chat_id=mock_message.chat.id,
        studios=expected_updated_studios,
    )

    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="Failed to find instructor(s): /, unknown",
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )

    mock_instructors_selection_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )


def test_instructors_selection_handler_selected(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test instructors_selection_handler with studios selected flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_studios = {
        StudioType.Rev: StudioData(
            locations=[StudioLocation.Bugis],
            instructors=["Rev Instructor"],
        )
    }
    test_query_data = QueryData(
        studios=test_studios,
        current_studio=StudioType.Anarchy,
        weeks=3,
        days=["Monday", "Wednesday", "Friday"],
        start_times=[],
        class_name_filter="",
    )

    # Setup mocks
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.get_query_data.return_value = test_query_data

    mock_instructors_keyboard = mocker.Mock()

    mock_keyboard_manager = mocker.Mock(spec=KeyboardManager)
    mock_keyboard_manager.get_instructors_keyboard.return_value = mock_instructors_keyboard

    # Call the function to test
    instructors_page_handler.instructors_selection_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="*Currently selected instructor(s)*\nInstructor(s):\nRev: Rev Instructor\n",
        reply_markup=mock_instructors_keyboard,
        delete_sent_msg_in_future=True,
    )


def test_instructors_selection_handler_no_studios_selected(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
) -> None:
    """
    Test instructors_selection_handler no studios selected flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.

    """
    test_query_data = QueryData(
        studios={},
        current_studio=StudioType.Anarchy,
        weeks=3,
        days=["Monday", "Wednesday", "Friday"],
        start_times=[],
        class_name_filter="",
    )

    # Setup mocks
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.get_query_data.return_value = test_query_data

    mock_keyboard_manager = mocker.Mock()

    mock_main_page_handler = mocker.patch("menu.instructors_page_handler.main_page_handler")

    # Call the function to test
    instructors_page_handler.instructors_selection_handler(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )

    # Assert that flow was called with the expected arguments
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text="No studio selected. Please select a studio first",
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )

    mock_main_page_handler.assert_called_once_with(
        message=mock_message,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
    )
