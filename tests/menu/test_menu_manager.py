"""
test_menu_manager.py
Author: https://github.com/lendrixxx
Description: This file tests the functions of the MenuManager class.
"""

from typing import Any, Callable, NamedTuple, Optional, TypeAlias
from unittest.mock import Mock

import pytest_mock

from menu.menu_manager import MenuManager


def test_constructor_calls_setup_handlers(
    mocker: pytest_mock.plugin.MockerFixture,
) -> None:
    """
    Test that MenuManager constructor calls setup_message_handlers and
    setup_callback_query_handlers.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_history_manager = mocker.Mock()
    mock_studios_manager = mocker.Mock()

    setup_messages_mock = mocker.patch("menu.menu_manager.MenuManager.setup_message_handlers")
    setup_callbacks_mock = mocker.patch("menu.menu_manager.MenuManager.setup_callback_query_handlers")

    # Call the constructor to test
    MenuManager(
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        history_manager=mock_history_manager,
        studios_manager=mock_studios_manager,
    )

    # Assert
    setup_messages_mock.assert_called_once()
    setup_callbacks_mock.assert_called_once()


class CallbackQueryHandlerData(NamedTuple):
    handler_name: str
    mock_handler: Mock
    expected_args: dict[str, Any]


class WrappedDecorator(NamedTuple):
    handler_func: Any
    kwargs: Any


HandlerFunc: TypeAlias = Callable[..., Any]
Decorator: TypeAlias = Callable[[HandlerFunc], HandlerFunc]
DecoratorFactory: TypeAlias = Callable[[Optional[HandlerFunc]], Decorator]


def new_decorator_wrapper(registered_handlers: dict[str, WrappedDecorator]) -> DecoratorFactory:
    def decorator_wrapper(func: Optional[HandlerFunc] = None, **kwargs: Any) -> Decorator:
        def wrapper(handler_func: HandlerFunc) -> HandlerFunc:
            decorator_name = handler_func.__name__
            registered_handlers[decorator_name] = WrappedDecorator(
                handler_func=handler_func,
                kwargs=kwargs,
            )
            return handler_func

        return wrapper

    return decorator_wrapper


def test_setup_callback_query_handlers(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_studios_manager: Mock,
) -> None:
    """
    Test that setup_callback_query_handlers registers and calls the handlers correctly.

    Args:
      - mocker: pytest-mock fixture for patching.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_history_manager = mocker.Mock()

    # Patch the target handlers and the expected args that the handler will be called with
    mock_callback_query_handlers = [
        CallbackQueryHandlerData(
            handler_name="main_page_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.main_page_handler.main_page_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'main-page-handler'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="studios_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.studios_page_handler.studios_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'studios'}"),
                "bot": mock_bot,
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="studios_selection_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.studios_page_handler.studios_selection_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'studios-selection'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="locations_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.studios_page_handler.locations_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'locations'}"),
                "bot": mock_bot,
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="instructors_selection_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.instructors_selection_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'instructors-selection'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="show_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.show_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'show-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "studios_manager": mock_studios_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="rev_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.rev_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'rev-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Rev"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="barrys_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.barrys_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'barrys-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Barrys"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="absolute_spin_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.absolute_spin_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'absolute-spin-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Absolute"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="absolute_pilates_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.absolute_pilates_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'absolute-pilates-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Absolute"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="ally_spin_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.ally_spin_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'ally-spin-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Ally"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="ally_pilates_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.ally_pilates_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'ally-pilates-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Ally"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="anarchy_instructors_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.instructors_page_handler.anarchy_instructors_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'anarchy-instructors'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "bot": mock_bot,
                "instructorid_map": mock_studios_manager.studios["Anarchy"].get_instructorid_map(),
            },
        ),
        CallbackQueryHandlerData(
            handler_name="weeks_selection_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.weeks_page_handler.weeks_selection_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'weeks-selection'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="weeks_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.weeks_page_handler.weeks_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'weeks'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="days_page_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.days_page_handler.days_page_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'days'}"),
                "bot": mock_bot,
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="days_selection_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.days_page_handler.days_selection_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'days-selection'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="days_next_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.days_page_handler.days_next_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'days-next'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="time_selection_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.time_page_handler.time_selection_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'time-selection'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="time_selection_add_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.time_page_handler.time_selection_add_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'time-selection-add'}"),
                "logger": mock_logger,
                "bot": mock_bot,
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="time_selection_remove_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.time_page_handler.time_selection_remove_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'time-selection-remove'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="time_selection_remove_timeslot_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.time_page_handler.time_selection_remove_timeslot_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'remove-timeslot'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="time_selection_reset_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.time_page_handler.time_selection_reset_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'time-selection-reset'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="class_name_filter_selection_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.name_filter_page_handler.class_name_filter_selection_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'class-name-filter-selection'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="class_name_filter_set_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.name_filter_page_handler.class_name_filter_set_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'class-name-filter-add'}"),
                "bot": mock_bot,
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="class_name_filter_reset_callback_query_handler",
            mock_handler=mocker.patch(
                "menu.menu_manager.name_filter_page_handler.class_name_filter_reset_callback_query_handler"
            ),
            expected_args={
                "query": mocker.Mock(data="{'step': 'class-name-filter-reset'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
            },
        ),
        CallbackQueryHandlerData(
            handler_name="get_schedule_callback_query_handler",
            mock_handler=mocker.patch("menu.menu_manager.get_schedule_handler.get_schedule_callback_query_handler"),
            expected_args={
                "query": mocker.Mock(data="{'step': 'get-schedule'}"),
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "full_result_data": mock_studios_manager.get_cached_result_data(),
            },
        ),
    ]

    # Instantiate MenuManager
    menu_manager = MenuManager(
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        history_manager=mock_history_manager,
        studios_manager=mock_studios_manager,
    )

    # Replace the decorator to store the decorated function
    registered_handlers: dict[str, WrappedDecorator] = {}
    mock_bot.callback_query_handler.side_effect = new_decorator_wrapper(registered_handlers)

    # Call the method that registers the handler
    menu_manager.setup_callback_query_handlers()

    # Assert that flow was called with the expected arguments
    assert len(registered_handlers) == 27

    for mock_callback_query_handler in mock_callback_query_handlers:
        # Simulate a callback query
        wrapped_decorator = registered_handlers[mock_callback_query_handler.handler_name]
        wrapped_decorator.handler_func(mock_callback_query_handler.expected_args["query"])

        # Assert the handler was called with expected args
        mock_callback_query_handler.mock_handler.assert_called_once_with(
            **mock_callback_query_handler.expected_args,
        )


class MessageHandlerData(NamedTuple):
    handler_name: str
    mock_handler: Mock
    expected_args: dict[str, Any]


def test_setup_message_handlers(
    mocker: pytest_mock.plugin.MockerFixture,
    mock_message: Mock,
    mock_studios_manager: Mock,
) -> None:
    """
    Test that setup_message_handlers registers and calls the handlers correctly.

    Args:
      - mocker: pytest-mock fixture for patching.
      - mock_message (Mock): Mock instance of telebot.types.Message.
      - mock_studios_manager (Mock): Mock instance of StudiosManager.

    """

    # Setup mocks
    mock_logger = mocker.Mock()
    mock_bot = mocker.Mock()
    mock_chat_manager = mocker.Mock()
    mock_keyboard_manager = mocker.Mock()
    mock_history_manager = mocker.Mock()

    # Patch the target handlers and the expected args that the handler will be called with
    mock_message_handlers = [
        MessageHandlerData(
            handler_name="start_message_handler",
            mock_handler=mocker.patch("menu.menu_manager.start_page_handler.start_message_handler"),
            expected_args={
                "message": mock_message,
                "chat_manager": mock_chat_manager,
                "keyboard_manager": mock_keyboard_manager,
                "history_manager": mock_history_manager,
            },
        ),
        MessageHandlerData(
            handler_name="nerd_message_handler",
            mock_handler=mocker.patch("menu.menu_manager.nerd_page_handler.nerd_message_handler"),
            expected_args={
                "message": mock_message,
                "logger": mock_logger,
                "bot": mock_bot,
                "chat_manager": mock_chat_manager,
                "history_manager": mock_history_manager,
                "studios_manager": mock_studios_manager,
                "full_result_data": mock_studios_manager.get_cached_result_data(),
            },
        ),
        MessageHandlerData(
            handler_name="instructors_message_handler",
            mock_handler=mocker.patch("menu.menu_manager.instructors_page_handler.instructors_message_handler"),
            expected_args={
                "message": mock_message,
                "chat_manager": mock_chat_manager,
                "history_manager": mock_history_manager,
                "studios_manager": mock_studios_manager,
            },
        ),
    ]

    # Instantiate MenuManager
    menu_manager = MenuManager(
        logger=mock_logger,
        bot=mock_bot,
        chat_manager=mock_chat_manager,
        keyboard_manager=mock_keyboard_manager,
        history_manager=mock_history_manager,
        studios_manager=mock_studios_manager,
    )

    # Replace the decorator to store the decorated function
    registered_handlers: dict[str, WrappedDecorator] = {}
    mock_bot.message_handler.side_effect = new_decorator_wrapper(registered_handlers)

    # Call the method that registers the handler
    menu_manager.setup_message_handlers()

    # Assert that flow was called with the expected arguments
    assert len(registered_handlers) == 3

    for mock_message_handler in mock_message_handlers:
        # Simulate a callback query
        wrapped_decorator = registered_handlers[mock_message_handler.handler_name]
        wrapped_decorator.handler_func(mock_message_handler.expected_args["message"])

        # Assert the handler was called with expected args
        mock_message_handler.mock_handler.assert_called_once_with(
            **mock_message_handler.expected_args,
        )
