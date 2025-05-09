"""
test_chat_manager.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the ChatManager class.
"""

import pytest_mock

from chat.chat_manager import ChatManager
from common.data import SORTED_DAYS, STUDIO_LOCATIONS_MAP
from common.query_data import QueryData
from common.studio_data import StudioData
from common.studio_type import StudioType


def test_init(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test initialization of ChatManager object.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Assert that the object is created as expected
    assert chat_manager.logger == mock_logger
    assert chat_manager.bot == mock_bot
    assert chat_manager.chat_query_data == {}
    assert chat_manager.chat_message_ids_to_delete == {}
    assert chat_manager.chat_messages_to_edit == {}


def test_reset_query_and_messages_to_edit_data(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test reset_query_and_messages_to_edit_data flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    test_chat_id = 1

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_query_data(test_chat_id) == QueryData(
        studios=None,
        current_studio=StudioType.Null,
        weeks=1,
        days=SORTED_DAYS,
        start_times=[],
        class_name_filter="",
    )

    assert test_chat_id in chat_manager.chat_messages_to_edit
    assert chat_manager.chat_messages_to_edit[test_chat_id] == ChatManager.MessagesToEdit()


def test_update_query_data_current_studio(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test update_query_data_current_studio flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    test_chat_id = 2
    test_current_studio = StudioType.Rev

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_query_data_current_studio(chat_id=test_chat_id, current_studio=test_current_studio)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_query_data(test_chat_id) == QueryData(
        studios=None,
        current_studio=test_current_studio,
        weeks=1,
        days=SORTED_DAYS,
        start_times=[],
        class_name_filter="",
    )


def test_update_query_data_studios(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test update_query_data_studios flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 2

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_query_data_studios(chat_id=test_chat_id, studios=sample_studios)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_query_data(test_chat_id) == QueryData(
        studios=sample_studios,
        current_studio=StudioType.Null,
        weeks=1,
        days=SORTED_DAYS,
        start_times=[],
        class_name_filter="",
    )


def test_update_query_data_select_all_studios(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test update_query_data_select_all_studios flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    test_chat_id = 3

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_query_data_select_all_studios(chat_id=test_chat_id)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_query_data(test_chat_id) == QueryData(
        studios={
            StudioType.Rev: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.Rev]),
            StudioType.Barrys: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.Barrys]),
            StudioType.AbsoluteSpin: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.AbsoluteSpin]),
            StudioType.AbsolutePilates: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.AbsolutePilates]),
            StudioType.AllySpin: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.AllySpin]),
            StudioType.AllyPilates: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.AllyPilates]),
            StudioType.AllyRecovery: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.AllyRecovery]),
            StudioType.Anarchy: StudioData(locations=STUDIO_LOCATIONS_MAP[StudioType.Anarchy]),
        },
        current_studio=StudioType.Null,
        weeks=1,
        days=SORTED_DAYS,
        start_times=[],
        class_name_filter="",
    )


def test_update_query_data_days(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test update_query_data_days flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_days = ["Monday", "Thursday", "Sunday"]

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_query_data_days(chat_id=test_chat_id, days=test_days)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_query_data(test_chat_id) == QueryData(
        studios=None,
        current_studio=StudioType.Null,
        weeks=1,
        days=test_days,
        start_times=[],
        class_name_filter="",
    )


def test_update_query_data_weeks(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test update_query_data_weeks flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_weeks = 3

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_query_data_weeks(chat_id=test_chat_id, weeks=test_weeks)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_query_data(test_chat_id) == QueryData(
        studios=None,
        current_studio=StudioType.Null,
        weeks=test_weeks,
        days=SORTED_DAYS,
        start_times=[],
        class_name_filter="",
    )


def test_update_studios_selection_message(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test update_studios_selection_message flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_studios_selection_message = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_studios_selection_message(
        chat_id=test_chat_id,
        studios_selection_message=mock_studios_selection_message,
    )

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_studios_selection_message(test_chat_id) == mock_studios_selection_message


def test_update_locations_selection_message(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test update_locations_selection_message flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_locations_selection_message = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_locations_selection_message(
        chat_id=test_chat_id,
        locations_selection_message=mock_locations_selection_message,
    )

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_locations_selection_message(test_chat_id) == mock_locations_selection_message


def test_update_days_selection_message(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test update_days_selection_message flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_days_selection_message = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.update_days_selection_message(
        chat_id=test_chat_id,
        days_selection_message=mock_days_selection_message,
    )

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_query_data
    assert chat_manager.get_days_selection_message(test_chat_id) == mock_days_selection_message


def test_add_message_id_to_delete(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test add_message_id_to_delete flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_message_id_1 = 1
    test_message_id_2 = 2

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    chat_manager.add_message_id_to_delete(chat_id=test_chat_id, message_id=test_message_id_1)
    chat_manager.add_message_id_to_delete(chat_id=test_chat_id, message_id=test_message_id_2)

    # Assert that the object values is as expected
    assert test_chat_id in chat_manager.chat_message_ids_to_delete
    assert chat_manager.chat_message_ids_to_delete[test_chat_id] == [test_message_id_1, test_message_id_2]


def test_send_prompt(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test send_prompt delete_sent_msg_in_future false flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_text = "test text"

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_bot.send_message.return_value = mock_sent_msg

    mock_logger = mocker.Mock()
    mock_reply_markup = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    sent_msg = chat_manager.send_prompt(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        delete_sent_msg_in_future=False,
    )

    # Assert that flow was called with the expected arguments
    mock_bot.send_message.assert_called_once_with(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        parse_mode="Markdown",
    )

    # Assert that the object values is as expected
    assert sent_msg == mock_sent_msg
    assert test_chat_id not in chat_manager.chat_message_ids_to_delete


def test_send_prompt_delete_sent_msg_in_future(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test send_prompt delete_sent_msg_in_future true flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_text = "test text"
    test_sent_msg_id = 5

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_sent_msg.id = test_sent_msg_id
    mock_bot = mocker.Mock()
    mock_bot.send_message.return_value = mock_sent_msg

    mock_logger = mocker.Mock()
    mock_reply_markup = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    sent_msg = chat_manager.send_prompt(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        delete_sent_msg_in_future=True,
    )

    # Assert that flow was called with the expected arguments
    mock_bot.send_message.assert_called_once_with(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        parse_mode="Markdown",
    )

    # Assert that the object values is as expected
    assert sent_msg == mock_sent_msg
    assert test_chat_id in chat_manager.chat_message_ids_to_delete
    assert chat_manager.chat_message_ids_to_delete[test_chat_id] == [test_sent_msg_id]


def test_send_prompt_with_msg_to_delete(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test send_prompt with message to delete flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_message_id_1 = 87
    test_message_id_2 = 44
    test_text = "test text"
    test_sent_msg_id = 5

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_sent_msg.id = test_sent_msg_id
    mock_bot = mocker.Mock()
    mock_bot.send_message.return_value = mock_sent_msg

    mock_logger = mocker.Mock()
    mock_reply_markup = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)
    chat_manager.add_message_id_to_delete(chat_id=test_chat_id, message_id=test_message_id_1)
    chat_manager.add_message_id_to_delete(chat_id=test_chat_id, message_id=test_message_id_2)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    sent_msg = chat_manager.send_prompt(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        delete_sent_msg_in_future=False,
    )

    # Assert that flow was called with the expected arguments
    mock_bot.delete_messages.assert_called_once_with(
        chat_id=test_chat_id,
        message_ids=[test_message_id_1, test_message_id_2],
    )

    mock_bot.send_message.assert_called_once_with(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        parse_mode="Markdown",
    )

    # Assert that the object values is as expected
    assert sent_msg == mock_sent_msg
    assert test_chat_id not in chat_manager.chat_message_ids_to_delete


def test_send_prompt_with_msg_to_delete_exception(
    mocker: pytest_mock.MockerFixture,
    sample_studios: dict[StudioType, StudioData],
) -> None:
    """
    Test send_prompt exception occurred when deleting message flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    """
    test_chat_id = 4
    test_message_id_1 = 87
    test_text = "test text"
    test_sent_msg_id = 5
    test_exception_message = "test exception"

    # Setup mocks
    mock_sent_msg = mocker.Mock()
    mock_sent_msg.id = test_sent_msg_id
    mock_bot = mocker.Mock()
    mock_bot.send_message.return_value = mock_sent_msg
    mock_bot.delete_messages.side_effect = Exception(test_exception_message)

    mock_logger = mocker.Mock()
    mock_reply_markup = mocker.Mock()

    # Create ResultData object
    chat_manager = ChatManager(logger=mock_logger, bot=mock_bot)
    chat_manager.add_message_id_to_delete(chat_id=test_chat_id, message_id=test_message_id_1)

    # Call the function to test
    chat_manager.reset_query_and_messages_to_edit_data(chat_id=test_chat_id)
    sent_msg = chat_manager.send_prompt(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        delete_sent_msg_in_future=False,
    )

    # Assert that flow was called with the expected arguments
    mock_bot.delete_messages.assert_called_once_with(chat_id=test_chat_id, message_ids=[test_message_id_1])
    mock_logger.warning.assert_called_once_with(f"Failed to delete messages - {test_exception_message}")

    mock_bot.send_message.assert_called_once_with(
        chat_id=test_chat_id,
        text=test_text,
        reply_markup=mock_reply_markup,
        parse_mode="Markdown",
    )

    # Assert that the object values is as expected
    assert sent_msg == mock_sent_msg
    assert test_chat_id not in chat_manager.chat_message_ids_to_delete
