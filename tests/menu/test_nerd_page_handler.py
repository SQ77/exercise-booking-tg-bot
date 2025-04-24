"""
test_nerd_page_handler.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the nerd page handler.
"""

from datetime import datetime
from typing import NamedTuple
from unittest.mock import Mock

import pytest
import pytest_mock

import menu.nerd_page_handler as nerd_page_handler
from chat.chat_manager import ChatManager
from common.query_data import QueryData
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType


def test_nerd_message_handler(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test nerd_message_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """
    test_time = 123.0

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    mock_time = mocker.patch("time.time", return_value=mocker.MagicMock(spec=float))
    mock_time.return_value = test_time

    mock_bot = mocker.Mock()
    mock_logger = mocker.Mock()
    mock_history_manager = mocker.Mock()

    # Call the function to test
    nerd_page_handler.nerd_message_handler(
        message=mock_message,
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        history_manager=mock_history_manager,
        studios_manager=mock_studios_manager,
        full_result_data=mock_studios_manager.get_cached_result_data(),
    )

    # Assert that flow was called with the expected arguments
    mock_history_manager.add.assert_called_once_with(
        timestamp=int(test_time),
        user_id=mock_message.from_user.id,
        chat_id=mock_message.chat.id,
        username=mock_message.from_user.username,
        first_name=mock_message.from_user.first_name,
        last_name=mock_message.from_user.last_name,
        command="nerd",
    )

    mock_chat_manager.add_message_id_to_delete.assert_called_once_with(
        chat_id=mock_message.chat.id,
        message_id=mock_message.id,
    )

    expected_text = (
        "Welcome to nerd mode 🤓\n"
        "\n"
        "*Enter your query in the following format:*\n"
        "Studio name\n"
        "Studio locations (comma separated)\n"
        "Instructor names (comma separated)\n"
        "(Repeat above for multiple studios)\n"
        "Weeks\n"
        "Days\n"
        "Timeslots (comma separated. enter 'nil' to ignore filters)\n"
        "Class Name Filter (enter 'nil' to ignore filters)\n"
        "\n"
        "*Studio names*: rev, barrys, absolute (spin), absolute (pilates), ally (spin), ally (pilates)\n"
        "*Studio locations*: orchard, tjpg, bugis, raffles, centrepoint, i12, "
        "millenia walk, star vista, great world, cross street\n"
        "*Instructors*: Use /instructors for list of instructors\n"
        "\n"
        "*e.g.*\n"
        "`rev\n"
        "bugis, orchard\n"
        "chloe, zai\n"
        "absolute (spin)\n"
        "raffles\n"
        "ria\n"
        "2\n"
        "monday, wednesday, saturday\n"
        "0700-0900, 1300-1500, 1800-2000\n"
        "essential\n`"
    )
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=expected_text,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )

    mock_bot.register_next_step_handler.assert_called_once_with(
        message=mock_sent_msg,
        callback=nerd_page_handler.nerd_input_handler,
        logger=mock_logger,
        chat_manager=mock_chat_manager,
        studios_manager=mock_studios_manager,
        full_result_data=mock_studios_manager.get_cached_result_data(),
    )


class NerdInputHandlerSuccessArgs(NamedTuple):
    message_text: str
    expected_query: QueryData


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            NerdInputHandlerSuccessArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\nnil\nnil",
                expected_query=QueryData(
                    studios={
                        StudioType.Rev: StudioData(locations=[StudioLocation.Bugis], instructors=["rev instructor a"]),
                    },
                    current_studio=StudioType.Null,
                    weeks=1,
                    days=["All"],
                    start_times=[],
                    class_name_filter="",
                ),
            ),
            id=str(
                "Studio = Rev, Location = Bugis, Instructors = [rev instructor a], Weeks = 1, Days = all, "
                "Timeslots = nil, Class name filter = nil",
            ),
        ),
        pytest.param(
            NerdInputHandlerSuccessArgs(
                message_text="barrys\norchard\nall\n2\nmonday\nnil\nnil",
                expected_query=QueryData(
                    studios={
                        StudioType.Barrys: StudioData(
                            locations=[StudioLocation.Orchard],
                            instructors=["All"],
                        ),
                    },
                    current_studio=StudioType.Null,
                    weeks=2,
                    days=["Monday"],
                    start_times=[],
                    class_name_filter="",
                ),
            ),
            id=str(
                "Studio = Barrys, Location = Orchard, Instructors = all, Weeks = 2, Days = monday, "
                "Timeslots = nil, Class name filter = nil",
            ),
        ),
        pytest.param(
            NerdInputHandlerSuccessArgs(
                message_text="absolute (spin)\nall\nall\n1\nmonday\n0800-0900\nnil",
                expected_query=QueryData(
                    studios={
                        StudioType.AbsoluteSpin: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        ),
                    },
                    current_studio=StudioType.Null,
                    weeks=1,
                    days=["Monday"],
                    start_times=[(datetime(1900, 1, 1, 8, 0), datetime(1900, 1, 1, 9, 0))],
                    class_name_filter="",
                ),
            ),
            id=str(
                "Studio = Absolute (Spin), Location = all, Instructors = all, Weeks = 1, Days = monday, "
                "Timeslots = 0800-0900, Class name filter = nil",
            ),
        ),
        pytest.param(
            NerdInputHandlerSuccessArgs(
                message_text="ally (pilates)\nall\nall\n1\nwednesday\nnil\ntest",
                expected_query=QueryData(
                    studios={
                        StudioType.AllyPilates: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        ),
                    },
                    current_studio=StudioType.Null,
                    weeks=1,
                    days=["Wednesday"],
                    start_times=[],
                    class_name_filter="test",
                ),
            ),
            id=str(
                "Studio = Ally (Pilates), Location = all, Instructors = all, Weeks = 1, Days = wednesday, "
                "Timeslots = nil, Class name filter = test",
            ),
        ),
        pytest.param(
            NerdInputHandlerSuccessArgs(
                message_text="anarchy\nall\nall\n1\nwednesday\nnil\nnil",
                expected_query=QueryData(
                    studios={
                        StudioType.Anarchy: StudioData(
                            locations=[StudioLocation.All],
                            instructors=["All"],
                        ),
                    },
                    current_studio=StudioType.Null,
                    weeks=1,
                    days=["Wednesday"],
                    start_times=[],
                    class_name_filter="",
                ),
            ),
            id=str(
                "Studio = Anarchy, Location = all, Instructors = all, Weeks = 1, Days = wednesday, "
                "Timeslots = nil, Class name filter = nil",
            ),
        ),
    ],
)
def test_nerd_input_handler_success_under_4095_chars(
    mocker: pytest_mock.plugin.MockerFixture,
    args: NerdInputHandlerSuccessArgs,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test nerd_input_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (NerdInputHandlerSuccessArgs): Provides arguments for the test case.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """
    test_result_str = "result"

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    mock_message.text = args.message_text

    mock_result = mocker.Mock()
    mock_result.get_result_str.return_value = test_result_str

    mock_full_result_data = mocker.Mock()
    mock_full_result_data.get_data.return_value = mock_result

    mock_logger = mocker.Mock()

    # Call the function to test
    nerd_page_handler.nerd_input_handler(
        message=mock_message,
        logger=mock_logger,
        chat_manager=mock_chat_manager,
        studios_manager=mock_studios_manager,
        full_result_data=mock_full_result_data,
    )

    # Assert that flow was called with the expected arguments
    mock_full_result_data.get_data.assert_called_once_with(query=args.expected_query)
    mock_result.get_result_str.assert_called_once()
    mock_chat_manager.send_prompt.assert_called_once_with(
        chat_id=mock_message.chat.id,
        text=test_result_str,
        reply_markup=None,
        delete_sent_msg_in_future=False,
    )


def test_nerd_input_handler_success_over_4095_chars(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test nerd_input_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """
    total_lines = 500
    lines_list = ["test_line"] * total_lines
    test_result_str = "\n".join(lines_list)

    expected_query = QueryData(
        studios={StudioType.Anarchy: StudioData(locations=[StudioLocation.All], instructors=["All"])},
        current_studio=StudioType.Null,
        weeks=1,
        days=["Wednesday"],
        start_times=[],
        class_name_filter="",
    )

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    mock_message.text = "anarchy\nall\nall\n1\nwednesday\nnil\nnil"

    mock_result = mocker.Mock()
    mock_result.get_result_str.return_value = test_result_str

    mock_full_result_data = mocker.Mock()
    mock_full_result_data.get_data.return_value = mock_result

    mock_logger = mocker.Mock()

    # Call the function to test
    nerd_page_handler.nerd_input_handler(
        message=mock_message,
        logger=mock_logger,
        chat_manager=mock_chat_manager,
        studios_manager=mock_studios_manager,
        full_result_data=mock_full_result_data,
    )

    # Assert that flow was called with the expected arguments
    mock_full_result_data.get_data.assert_called_once_with(query=expected_query)
    mock_result.get_result_str.assert_called_once()

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


class NerdInputHandlerFailureArgs(NamedTuple):
    message_text: str
    expected_error_texts: list[str]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="invalid\nnerd\ninput",
                expected_error_texts=["Failed to handle query. Unexpected format received."],
            ),
            id="Invalid input string rows",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="test studio\nall\nall\n1\nall\nnil\nnil",
                expected_error_texts=["Failed to handle query. Unexpected studio name 'test studio'"],
            ),
            id="Invalid studio",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\ntest location\nall\n1\nall\nnil\nnil",
                expected_error_texts=["Failed to handle query. Unexpected studio location 'test location'"],
            ),
            id="Invalid studio location",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nunknown instructor\n1\nall\nnil\nnil",
                expected_error_texts=[
                    "Failed to find instructor(s): unknown instructor",
                    "Failed to handle query. No instructor selected for Rev",
                ],
            ),
            id="Invalid instructor",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\nabc\nall\nnil\nnil",
                expected_error_texts=[
                    "Failed to handle query. Invalid input for 'weeks'. Expected number, got abc - "
                    "invalid literal for int() with base 10: 'abc'",
                ],
            ),
            id="Invalid weeks",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nSomeday\nnil\nnil",
                expected_error_texts=[
                    "Failed to handle query. Invalid input for 'days'. Unknown day Someday",
                ],
            ),
            id="Invalid day",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n2359\nnil",
                expected_error_texts=[
                    "Failed to handle query. Invalid input for 'timeslots'. '2359' is not a valid timeslot",
                ],
            ),
            id="Invalid timeslot - Not valid range",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n12345-2359\nnil",
                expected_error_texts=[
                    "Failed to handle query. Invalid input for 'timeslots'. Start time '12345' is not valid",
                ],
            ),
            id="Invalid timeslot - Invalid start time length",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n0000-50000\nnil",
                expected_error_texts=[
                    "Failed to handle query. Invalid input for 'timeslots'. End time '50000' is not valid",
                ],
            ),
            id="Invalid timeslot - Invalid end time length",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n4567-2359\nnil",
                expected_error_texts=[
                    "Invalid time '4567' entered. Please enter time in 24 hour format",
                ],
            ),
            id="Invalid timeslot - Invalid start time",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n0000-2799\nnil",
                expected_error_texts=[
                    "Invalid time '2799' entered. Please enter time in 24 hour format",
                ],
            ),
            id="Invalid timeslot - Invalid end time",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n1600-1330\nnil",
                expected_error_texts=[
                    "Failed to handle query. Invalid input for 'timeslots'. "
                    "Start time '1600' is later than end time '1330'"
                ],
            ),
            id="Invalid timeslot - End time earlier than start time",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n0800-1000,0830-1030\nnil",
                expected_error_texts=["Start time '0830' conflicts with existing timeslot '0800 - 1000'"],
            ),
            id="Invalid timeslot - Start time falls within existing timeslot",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n0800-0800,0800-0800\nnil",
                expected_error_texts=["Start time '0800' conflicts with existing timeslot '0800 - 0800'"],
            ),
            id="Invalid timeslot - Duplicate timeslots",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n0800-0900,0700-0830\nnil",
                expected_error_texts=["End time '0830' conflicts with existing timeslot '0800 - 0900'"],
            ),
            id="Invalid timeslot - End time falls within existing timeslot",
        ),
        pytest.param(
            NerdInputHandlerFailureArgs(
                message_text="rev\nbugis\nrev instructor a\n1\nall\n0800-0900,0700-0930\nnil",
                expected_error_texts=["Time range '0700 - 0930' conflicts with existing timeslot '0800 - 0900'"],
            ),
            id="Invalid timeslot - Timeslot contains existing timeslot",
        ),
    ],
)
def test_nerd_input_handler_failures(
    mocker: pytest_mock.plugin.MockerFixture,
    args: NerdInputHandlerFailureArgs,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test nerd_input_handler flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (NerdInputHandlerFailureArgs): Provides arguments for the test case.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """
    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_chat_manager = mocker.Mock(spec=ChatManager)
    mock_chat_manager.send_prompt.return_value = mock_sent_msg

    mock_message.text = args.message_text

    mock_logger = mocker.Mock()

    # Call the function to test
    nerd_page_handler.nerd_input_handler(
        message=mock_message,
        logger=mock_logger,
        chat_manager=mock_chat_manager,
        studios_manager=mock_studios_manager,
        full_result_data=mock_studios_manager.get_cached_result_data(),
    )

    # Assert that flow was called with the expected arguments
    expected_send_prompt_calls = []
    for expected_error_text in args.expected_error_texts:
        expected_send_prompt_calls.append(
            mocker.call(
                chat_id=mock_message.chat.id,
                text=expected_error_text,
                reply_markup=None,
                delete_sent_msg_in_future=False,
            )
        )
    assert mock_chat_manager.send_prompt.call_args_list == expected_send_prompt_calls
