"""
test_history_manager.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the HistoryManager class.
"""

import pytest_mock

from history.history_manager import HistoryManager


def test_history_manager_initialization(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test HistoryManager initialization.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """

    # Setup mocks
    mock_logger = mocker.Mock()

    # Create HistoryManager object
    history_manager = HistoryManager(logger=mock_logger)

    # Assert that the object is created as expected
    assert history_manager.logger == mock_logger
    assert history_manager.file_path == "booking-bot-history.csv"
    assert history_manager.headers == [
        "timestamp",
        "user_id",
        "chat_id",
        "username",
        "first_name",
        "last_name",
        "command",
    ]


def test_start_file_exists_headers_match(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test start history file exists with matching headers flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_os_path_exists = mocker.patch("history.history_manager.os.path.exists")
    mock_os_path_exists.return_value = True

    mock_file = mocker.Mock()
    mock_file.readline.return_value = "timestamp,user_id,chat_id,username,first_name,last_name,command"
    mock_open = mocker.patch("history.history_manager.open")
    mock_open.return_value = mock_file

    # Create HistoryManager object
    history_manager = HistoryManager(logger=mock_logger)

    # Call the function to test
    history_manager.start()

    # Assert that flow was called with the expected arguments
    mock_logger.info.assert_called_once_with(
        f"Found existing history file {history_manager.file_path}. Loading contents..."
    )
    mock_open.assert_called_once_with(history_manager.file_path, "r")
    mock_file.close.assert_called_once_with()


def test_start_file_exists_headers_do_not_match(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test start history file exists with non-matching headers flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    test_existing_header_line = "username,command"
    test_existing_headers = test_existing_header_line.strip("\n").split(",")
    test_time = 988.0
    test_rename_file_path = f"booking-bot-history-{int(test_time)}.csv"

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_os_path_exists = mocker.patch("history.history_manager.os.path.exists")
    mock_os_path_exists.side_effect = [True, False]

    mock_file = mocker.Mock()
    mock_file.readline.return_value = test_existing_header_line
    mock_open = mocker.patch("history.history_manager.open")
    mock_open.return_value = mock_file

    mock_time = mocker.patch("history.history_manager.time.time")
    mock_time.return_value = test_time

    mock_os_rename = mocker.patch("history.history_manager.os.rename")

    # Create HistoryManager object
    history_manager = HistoryManager(logger=mock_logger)

    # Call the function to test
    history_manager.start()

    # Assert that flow was called with the expected arguments
    expected_logger_info_calls = [
        mocker.call(f"Found existing history file {history_manager.file_path}. Loading contents..."),
        mocker.call(f"History file {history_manager.file_path} not found. Creating new file..."),
    ]
    assert mock_logger.info.call_args_list == expected_logger_info_calls

    mock_logger.warning.assert_called_once_with(
        f"Existing headers do not match current headers. Existing: {test_existing_headers}, "
        f"Current: {history_manager.headers}. Renaming existing file to {test_rename_file_path}..."
    )

    expected_open_calls = [
        mocker.call(history_manager.file_path, "r"),
        mocker.call(history_manager.file_path, "w"),
    ]
    assert mock_open.call_args_list == expected_open_calls

    expected_file_close_calls = [
        mocker.call(),
        mocker.call(),
    ]
    assert mock_file.close.call_args_list == expected_file_close_calls

    expected_file_write_calls = [
        mocker.call(",".join(history_manager.headers)),
        mocker.call("\n"),
    ]
    assert mock_file.write.call_args_list == expected_file_write_calls

    mock_os_rename.assert_called_once_with(history_manager.file_path, test_rename_file_path)


def test_start_file_does_not_exist(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test start history file does not exist flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_os_path_exists = mocker.patch("history.history_manager.os.path.exists")
    mock_os_path_exists.return_value = False

    mock_file = mocker.Mock()
    mock_open = mocker.patch("history.history_manager.open")
    mock_open.return_value = mock_file

    # Create HistoryManager object
    history_manager = HistoryManager(logger=mock_logger)

    # Call the function to test
    history_manager.start()

    # Assert that flow was called with the expected arguments
    mock_logger.info.assert_called_once_with(
        f"History file {history_manager.file_path} not found. Creating new file..."
    )
    mock_open.assert_called_once_with(history_manager.file_path, "w")

    expected_file_write_calls = [
        mocker.call(",".join(history_manager.headers)),
        mocker.call("\n"),
    ]
    assert mock_file.write.call_args_list == expected_file_write_calls

    mock_file.close.assert_called_once_with()


def test_add(
    mocker: pytest_mock.MockerFixture,
) -> None:
    """
    Test add flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    test_timestamp = 111
    test_user_id = 222
    test_chat_id = 333
    test_username = "test username"
    test_first_name = "test first name"
    test_last_name = "test last name"
    test_command = "test command"

    # Setup mocks
    mock_logger = mocker.Mock()

    mock_file = mocker.Mock()
    mock_open = mocker.patch("history.history_manager.open")
    mock_open.return_value = mock_file

    # Create HistoryManager object
    history_manager = HistoryManager(logger=mock_logger)

    # Call the function to test
    history_manager.add(
        timestamp=test_timestamp,
        user_id=test_user_id,
        chat_id=test_chat_id,
        username=test_username,
        first_name=test_first_name,
        last_name=test_last_name,
        command=test_command,
    )

    # Assert that flow was called with the expected arguments
    mock_logger.info.assert_called_once_with(
        f"New request - user_id: {test_user_id}, chat_id: {test_chat_id}, username: {test_username}, "
        f"first_name: {test_first_name}, last_name: {test_last_name}, command: {test_command}"
    )
    mock_open.assert_called_once_with(history_manager.file_path, "a")
    mock_file.write.assert_called_once_with(
        f"{test_timestamp}, {test_user_id}, {test_chat_id}, {test_username}, "
        f"{test_first_name}, {test_last_name}, {test_command}\n"
    )
    mock_file.close.assert_called_once_with()
