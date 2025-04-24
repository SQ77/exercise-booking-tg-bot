"""
conftest.py
Author: https://github.com/lendrixxx
Description: This file contains pytest configuration, fixtures, and other shared test utilities
             that can be used across multiple test files.

"""

import inspect
from datetime import datetime
from pathlib import Path
from typing import Callable
from unittest.mock import Mock

import pytest
import pytest_mock
import telebot

from common.query_data import QueryData
from common.studio_data import StudioData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from studios.studios_manager import StudiosManager


@pytest.fixture
def load_response_file() -> Callable[[str], str]:
    """
    Fixture to get a function that loads a file from the "example_responses" directory
    located next to the test file calling this fixture.

    Args:
      - filename (str): Name of the file to load.
        e.g. Loads "tests/studios/ally/example_responses/{filename}" if called from "tests/studios/ally/test_ally.py"

    Returns:
      - Callable[[str], str]: Function that returns the contents of the specified file as a string.

    """

    def _load(filename: str) -> str:
        """
        Function to load a file from the "example_responses" directory located next to
        the test file calling this function.

        Args:
          - filename (str): Name of the file to load.
            e.g. Loads "tests/studios/ally/example_responses/{filename}"
                 if called from "tests/studios/ally/test_ally.py"

        Returns:
          - Callable[[str], str]: Function that returns the contents of the specified file as a string.

        """
        # Determine the test file calling this function
        try:
            test_file = Path(inspect.stack()[1].filename)
        except IndexError:
            raise RuntimeError("Failed to resolve test file path for load_response_file fixture.")

        path = test_file.parent / "example_responses" / filename
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        return path.read_text(encoding="utf-8")

    return _load


@pytest.fixture
def sample_studios() -> dict[StudioType, StudioData]:
    """
    Fixture to create sample studio data.

    Returns:
        Dictionary of studios and studio data.

    """
    return {
        StudioType.AbsoluteSpin: StudioData(
            locations=[StudioLocation.Orchard, StudioLocation.Raffles],
            instructors=["Absolute Instructor", "Spin Instructor"],
        ),
        StudioType.Rev: StudioData(locations=[StudioLocation.Bugis], instructors=["Rev Instructor"]),
    }


@pytest.fixture
def sample_empty_query_data() -> QueryData:
    """
    Fixture to create an empty sample QueryData instance.

    Returns:
        QueryData: Empty query data.

    """
    return QueryData(
        studios={},
        current_studio=StudioType.AbsoluteSpin,
        weeks=2,
        days=[],
        start_times=[],
        class_name_filter="",
    )


@pytest.fixture
def sample_query_data(sample_studios: dict[StudioType, StudioData]) -> QueryData:
    """
    Fixture to create a sample QueryData instance.

    Args:
      - sample_studios (dict[StudioType, StudioData]): Dictionary of studios and studio data to use for the QueryData.

    Returns:
        QueryData: Query data with the specified studios.

    """
    start_time = datetime.strptime("06:00", "%H:%M")
    end_time = datetime.strptime("07:00", "%H:%M")

    return QueryData(
        studios=sample_studios,
        current_studio=StudioType.AbsoluteSpin,
        weeks=3,
        days=["Monday", "Wednesday", "Friday"],
        start_times=[(start_time, end_time)],
        class_name_filter="RIDE",
    )


@pytest.fixture
def mock_message(mocker: pytest_mock.plugin.MockerFixture) -> Mock:
    """
    Creates a mock object with telebot.types.Message spec.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    Returns:
      - Mock: Mock object simulating a telebot.types.Message object.

    """
    mock_chat_obj = Mock(spec=telebot.types.Chat, id=1)
    mock_from_user_obj = Mock(
        spec=telebot.types.User,
        id=2,
        username="user",
        first_name="test_first_name",
        last_name="test_last_name",
    )
    return Mock(spec=telebot.types.Message, id=3, chat=mock_chat_obj, from_user=mock_from_user_obj)


@pytest.fixture
def mock_studios_manager(mocker: pytest_mock.plugin.MockerFixture) -> Mock:
    """
    Creates a mock object with StudiosManager spec.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    Returns:
      - Mock: Mock object simulating a StudiosManager object.

    """

    def new_mock_studio_manager(studio_name: str) -> mocker.Mock:
        mock_studio_manager = mocker.Mock()
        mock_studio_manager.get_instructor_names.return_value = [
            f"{studio_name} Instructor A".lower(),
            f"{studio_name} Instructor B".lower(),
        ]
        return mock_studio_manager

    mock_studios_manager = mocker.Mock(
        spec=StudiosManager,
        studios={
            "Rev": new_mock_studio_manager("Rev"),
            "Barrys": new_mock_studio_manager("Barrys"),
            "Absolute": new_mock_studio_manager("Absolute"),
            "Ally": new_mock_studio_manager("Ally"),
            "Anarchy": new_mock_studio_manager("Anarchy"),
        },
    )
    return mock_studios_manager
