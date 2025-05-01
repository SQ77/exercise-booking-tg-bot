"""
test_server.py
Author: https://github.com/lendrixxx
Description: This file tests the implementation of the Server class.
"""

import pytest
import pytest_mock
import requests

from server.server import Server


@pytest.fixture
def mock_server(mocker: pytest_mock.plugin.MockerFixture) -> Server:
    """
    Creates a server with mocks for testing.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking..

    """
    return Server(
        logger=mocker.Mock(),
        bot=mocker.Mock(),
        base_url="http://localhost:5000",
        port=5000,
        webhook_path="webhook",
    )


def test_home(mock_server: Server) -> None:
    """
    Test ping /home.

    Args:
      - mock_server (Server): Server to use for test.

    """
    # Ping the endpoint to test
    client = mock_server.app.test_client()
    response = client.get("/")

    # Assert that the response is as expected
    assert response.status_code == 200
    assert response.data.decode() == "Server is running"


def test_health(mock_server: Server) -> None:
    """
    Test ping /health.

    Args:
      - mock_server (Server): Server to use for test.

    """
    # Ping the endpoint to test
    client = mock_server.app.test_client()
    response = client.get("/health")

    # Assert that the response is as expected
    assert response.status_code == 200
    assert response.data.decode() == "OK"


def test_webhook(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_server: Server,
) -> None:
    """
    Test ping /webhook with update flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_server (Server): Server to use for test.

    """
    test_parsed_update = "parsed_update"

    # Setup mocks
    mock_update = {"update_id": 123}
    mocked_telebot_update = mocker.patch("telebot.types.Update.de_json", return_value=test_parsed_update)

    # Ping the endpoint to test
    client = mock_server.app.test_client()
    response = client.post("/webhook", json=mock_update)

    # Assert that flow was called with the expected arguments
    mocked_telebot_update.assert_called_once_with(mock_update)
    mock_server.bot.process_new_updates.assert_called_once_with([test_parsed_update])

    # Assert that the response is as expected
    assert response.status_code == 200
    assert response.data.decode() == "OK"


def test_ping_self_success(mocker: pytest_mock.plugin.MockerFixture, mock_server: Server) -> None:
    """
    Test ping_self success flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_server (Server): Server to use for test.

    """
    # Setup mocks
    mock_response = mocker.Mock(status_code=200)
    mocker.patch("requests.get", return_value=mock_response)

    # Call the function to test
    mock_server.ping_self()

    # Assert that flow was called with the expected arguments
    mock_server.logger.info.assert_called_once_with(f"Successfully pinged self {mock_server.health_check_url}.")


def test_ping_self_error_500(mocker: pytest_mock.plugin.MockerFixture, mock_server: Server) -> None:
    """
    Test ping_self error 500 flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_server (Server): Server to use for test.

    """
    # Setup mocks
    mock_response = mocker.Mock(status_code=500)
    mocker.patch("requests.get", return_value=mock_response)

    # Call the function to test
    mock_server.ping_self()

    # Assert that flow was called with the expected arguments
    mock_server.logger.warning.assert_called_once_with("Unexpected response from server: 500")


def test_ping_self_exception(mocker: pytest_mock.plugin.MockerFixture, mock_server: Server) -> None:
    """
    Test ping_self exception flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_server (Server): Server to use for test.

    """
    test_exception_message = "Connection failed"
    # Setup mocks
    mock_get = mocker.patch("requests.get", side_effect=requests.exceptions.RequestException(test_exception_message))

    # Call the function to test
    mock_server.ping_self()

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(url=mock_server.health_check_url)
    mock_server.logger.error.assert_called_once_with(f"Failed to reach self: {test_exception_message}")
    mock_server.logger.info.assert_not_called()
    mock_server.logger.warning.assert_not_called()


def test_start_server(mocker: pytest_mock.plugin.MockerFixture, mock_server: Server) -> None:
    """
    Test start_server exception flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - mock_server (Server): Server to use for test.

    """
    # Setup mocks
    mock_run = mocker.patch.object(mock_server.app, "run")

    # Call the function to test
    mock_server.start_server()

    # Assert that flow was called with the expected arguments
    mock_server.logger.info.assert_called_once_with(f"Starting server on {mock_server.base_url}")
    mock_run.assert_called_once()
