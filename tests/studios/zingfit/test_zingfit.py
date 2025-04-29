"""
test_zingfit.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Zingfit.
"""

import logging
from datetime import date
from typing import Callable, NamedTuple, Optional

import pytest
import pytest_mock
from bs4 import BeautifulSoup

from common.class_data import ClassData
from common.result_data import ResultData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from studios.zingfit.data.absolute import LOCATION_TO_SITE_ID_MAP as ABSOLUTE_LOCATION_TO_SITE_ID_MAP
from studios.zingfit.data.absolute import MAX_SCHEDULE_WEEKS as ABSOLUTE_MAX_WEEKS
from studios.zingfit.data.absolute import ROOM_ID_TO_STUDIO_LOCATION_MAP as ABSOLUTE_ROOM_ID_TO_STUDIO_LOCATION_MAP
from studios.zingfit.data.absolute import ROOM_ID_TO_STUDIO_TYPE_MAP as ABSOLUTE_ROOM_ID_TO_STUDIO_TYPE_MAP
from studios.zingfit.data.absolute import TABLE_HEADING_DATE_FORMAT as ABSOLUTE_TABLE_HEADING_DATE_FORMAT
from studios.zingfit.data.absolute import URL_SUBDOMAIN as ABSOLUTE_URL_SUBDOMAIN
from studios.zingfit.data.ally import LOCATION_TO_SITE_ID_MAP as ALLY_LOCATION_TO_SITE_ID_MAP
from studios.zingfit.data.ally import MAX_SCHEDULE_WEEKS as ALLY_MAX_WEEKS
from studios.zingfit.data.ally import ROOM_ID_TO_STUDIO_LOCATION_MAP as ALLY_ROOM_ID_TO_STUDIO_LOCATION_MAP
from studios.zingfit.data.ally import ROOM_ID_TO_STUDIO_TYPE_MAP as ALLY_ROOM_ID_TO_STUDIO_TYPE_MAP
from studios.zingfit.data.ally import TABLE_HEADING_DATE_FORMAT as ALLY_TABLE_HEADING_DATE_FORMAT
from studios.zingfit.data.ally import URL_SUBDOMAIN as ALLY_URL_SUBDOMAIN
from studios.zingfit.data.ally import clean_class_name as ally_clean_class_name_func
from studios.zingfit.zingfit import (
    get_instructorid_map_from_response_soup,
    get_schedule_from_response_soup,
    get_zingfit_schedule_and_instructorid_map,
    send_get_schedule_request,
)
from tests.studios.zingfit.expected_results import (
    absolute_expected_results,
    ally_expected_results,
)


class GetScheduleTestArgs(NamedTuple):
    response_file_name: str
    table_heading_date_format: str
    room_id_to_studio_type_map: dict[str, StudioType]
    room_id_to_studio_location_map: dict[str, StudioLocation]
    clean_class_name_func: Optional[Callable[[str], str]]
    expected_result: dict[date, ClassData]


class GetInstructorIDTestArgs(NamedTuple):
    response_file_name: str
    expected_result: dict[str, str]


def test_send_get_schedule_request_single_location(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow with a single location.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200

    # Call the function to test
    location_to_site_id_map = {StudioLocation.Centrepoint: 1}
    locations = list(location_to_site_id_map)
    week = 1
    response = send_get_schedule_request(
        studio_url_subdomain=ABSOLUTE_URL_SUBDOMAIN,
        locations=locations,
        location_to_site_id_map=location_to_site_id_map,
        week=week,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url=f"https://{ABSOLUTE_URL_SUBDOMAIN}.zingfit.com/reserve/index.cfm",
        params={
            "wk": week,
            "site": location_to_site_id_map[locations[0]],
            "action": "Reserve.chooseClass",
        },
    )
    assert response.status_code == 200


def test_send_get_schedule_request_multiple_locations(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow with multiple locations.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200

    # Call the function to test
    location_to_site_id_map = {
        StudioLocation.Centrepoint: 1,
        StudioLocation.StarVista: 2,
        StudioLocation.MilleniaWalk: 3,
        StudioLocation.i12: 5,
        StudioLocation.GreatWorld: 6,
    }
    locations = list(location_to_site_id_map)
    week = 2
    response = send_get_schedule_request(
        studio_url_subdomain=ABSOLUTE_URL_SUBDOMAIN,
        locations=locations,
        location_to_site_id_map=location_to_site_id_map,
        week=week,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url=f"https://{ABSOLUTE_URL_SUBDOMAIN}.zingfit.com/reserve/index.cfm",
        params={
            "wk": week,
            "site": location_to_site_id_map[locations[0]],
            "site2": location_to_site_id_map[locations[1]],
            "site3": location_to_site_id_map[locations[2]],
            "site4": location_to_site_id_map[locations[3]],
            "site5": location_to_site_id_map[locations[4]],
            "action": "Reserve.chooseClass",
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetScheduleTestArgs(
                response_file_name="absolute_raffles_6_to_12_apr.html",
                table_heading_date_format=ABSOLUTE_TABLE_HEADING_DATE_FORMAT,
                room_id_to_studio_type_map=ABSOLUTE_ROOM_ID_TO_STUDIO_TYPE_MAP,
                room_id_to_studio_location_map=ABSOLUTE_ROOM_ID_TO_STUDIO_LOCATION_MAP,
                clean_class_name_func=None,
                expected_result=absolute_expected_results.EXPECTED_RAFFLES_6_TO_12_APR_SCHEDULE,
            ),
            id="Absolute Raffles 6 to 12 April",
        ),
        pytest.param(
            GetScheduleTestArgs(
                response_file_name="ally_crossstreet_7_to_13_apr.html",
                table_heading_date_format=ALLY_TABLE_HEADING_DATE_FORMAT,
                room_id_to_studio_type_map=ALLY_ROOM_ID_TO_STUDIO_TYPE_MAP,
                room_id_to_studio_location_map=ALLY_ROOM_ID_TO_STUDIO_LOCATION_MAP,
                clean_class_name_func=ally_clean_class_name_func,
                expected_result=ally_expected_results.EXPECTED_CROSSSTREET_7_TO_13_APR_SCHEDULE,
            ),
            id="Ally Cross Street 7 to 13 April",
        ),
    ],
)
def test_get_schedule_from_response_soup_single_location(
    mocker: pytest_mock.plugin.MockerFixture,
    load_response_file: Callable[[str], str],
    args: GetScheduleTestArgs,
) -> None:
    """
    Test get_schedule_from_response_soup flow with a single location.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.
      - args (GetScheduleTestArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file(args.response_file_name), "html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(
        logger=mock_logger,
        soup=mock_soup,
        studio_name="test studio",
        table_heading_date_format=args.table_heading_date_format,
        room_id_to_studio_type_map=args.room_id_to_studio_type_map,
        room_id_to_studio_location_map=args.room_id_to_studio_location_map,
        clean_class_name_func=args.clean_class_name_func,
    )

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == args.expected_result.keys()
    for key in result:
        assert result[key] == args.expected_result[key], (
            f"Expected result list {args.expected_result[key]} " f"does not match actual result list {result[key]}."
        )


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetScheduleTestArgs(
                response_file_name="absolute_milleniawalk_and_i12_7_to_12_apr.html",
                table_heading_date_format=ABSOLUTE_TABLE_HEADING_DATE_FORMAT,
                room_id_to_studio_type_map=ABSOLUTE_ROOM_ID_TO_STUDIO_TYPE_MAP,
                room_id_to_studio_location_map=ABSOLUTE_ROOM_ID_TO_STUDIO_LOCATION_MAP,
                clean_class_name_func=None,
                expected_result=absolute_expected_results.EXPECTED_MW_AND_I12_7_TO_12_APR_SCHEDULE,
            ),
            id="Absolute Millenia Walk and i12 7 to 12 April",
        ),
        pytest.param(
            GetScheduleTestArgs(
                response_file_name="ally_crossstreet_and_maxwell_6_to_12_may.html",
                table_heading_date_format=ALLY_TABLE_HEADING_DATE_FORMAT,
                room_id_to_studio_type_map=ALLY_ROOM_ID_TO_STUDIO_TYPE_MAP,
                room_id_to_studio_location_map=ALLY_ROOM_ID_TO_STUDIO_LOCATION_MAP,
                clean_class_name_func=ally_clean_class_name_func,
                expected_result=ally_expected_results.EXPECTED_CROSSSTREET_AND_MAXWELL_6_TO_12_MAY_SCHEDULE,
            ),
            id="Ally Cross Street and Maxwell 6 to 12 May",
        ),
    ],
)
def test_get_schedule_from_response_soup_multiple_locations(
    mocker: pytest_mock.plugin.MockerFixture,
    load_response_file: Callable[[str], str],
    args: GetScheduleTestArgs,
) -> None:
    """
    Test get_schedule_from_response_soup flow with multiple locations.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.
      - args (GetScheduleTestArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file(args.response_file_name), "html.parser")

    # Call the function to test
    result = get_schedule_from_response_soup(
        logger=mock_logger,
        soup=mock_soup,
        studio_name="test studio",
        table_heading_date_format=args.table_heading_date_format,
        room_id_to_studio_type_map=args.room_id_to_studio_type_map,
        room_id_to_studio_location_map=args.room_id_to_studio_location_map,
        clean_class_name_func=args.clean_class_name_func,
    )

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == args.expected_result.keys()
    for key in result:
        assert result[key] == args.expected_result[key], (
            f"Expected result list {args.expected_result[key]} " f"does not match actual result list {result[key]}."
        )


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetInstructorIDTestArgs(
                response_file_name="absolute_raffles_6_to_12_apr.html",
                expected_result=absolute_expected_results.EXPECTED_RAFFLES_6_TO_12_APR_INSTRUCTORID_MAP,
            ),
            id="Absolute Raffles 6 to 12 April",
        ),
        pytest.param(
            GetInstructorIDTestArgs(
                response_file_name="ally_crossstreet_7_to_13_apr.html",
                expected_result=ally_expected_results.EXPECTED_CROSSSTREET_7_TO_13_APR_INSTRUCTORID_MAP,
            ),
            id="Ally Cross Street 7 to 13 April",
        ),
    ],
)
def test_get_instructorid_map_from_response_soup_single_location(
    mocker: pytest_mock.plugin.MockerFixture,
    load_response_file: Callable[[str], str],
    args: GetInstructorIDTestArgs,
) -> None:
    """
    Test get_instructorid_map_from_response_soup flow with a single location.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.
      - args (GetInstructorIDTestArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file(args.response_file_name), "html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(
        logger=mock_logger, soup=mock_soup, studio_name="test studio"
    )

    # Assert that the response is as expected
    assert instructorid_map == args.expected_result


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetInstructorIDTestArgs(
                response_file_name="absolute_milleniawalk_and_i12_7_to_12_apr.html",
                expected_result=absolute_expected_results.EXPECTED_MW_AND_I12_7_TO_12_APR_INSTRUCTORID_MAP,
            ),
            id="Absolute Millenia Walk and i12 7 to 12 April",
        ),
        pytest.param(
            GetInstructorIDTestArgs(
                response_file_name="ally_crossstreet_and_maxwell_6_to_12_may.html",
                expected_result=ally_expected_results.EXPECTED_CROSSSTREET_AND_MAXWELL_6_TO_12_MAY_INSTRUCTORID_MAP,
            ),
            id="Ally Cross Street and Maxwell 6 to 12 May",
        ),
    ],
)
def test_get_instructorid_map_from_response_soup_multiple_locations(
    mocker: pytest_mock.plugin.MockerFixture,
    load_response_file: Callable[[str], str],
    args: GetInstructorIDTestArgs,
) -> None:
    """
    Test get_instructorid_map_from_response_soup flow with a multiple locations.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.
      - args (GetInstructorIDTestArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_soup = BeautifulSoup(load_response_file(args.response_file_name), "html.parser")

    # Call the function to test
    instructorid_map = get_instructorid_map_from_response_soup(
        logger=mock_logger, soup=mock_soup, studio_name="test studio"
    )

    # Assert that the response is as expected
    assert instructorid_map == args.expected_result


def test_get_zingfit_schedule_and_instructorid_map_absolute_flow(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_zingfit_schedule_and_instructorid_map flow for absolute.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_week_0_first_request_response = mocker.Mock()
    mock_week_0_first_request_response.text = load_response_file("absolute_centrepoint_7_to_13_apr.html")

    mock_week_0_second_request_response = mocker.Mock()
    mock_week_0_second_request_response.text = load_response_file("absolute_greatworld_8_to_13_apr.html")

    mock_week_1_first_request_response = mocker.Mock()
    mock_week_1_first_request_response.text = load_response_file("absolute_centrepoint_14_to_20_apr.html")

    mock_week_1_second_request_response = mocker.Mock()
    mock_week_1_second_request_response.text = load_response_file("absolute_greatworld_14_to_20_apr.html")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_week_0_first_request_response,
            mock_week_0_second_request_response,
            mock_week_1_first_request_response,
            mock_week_1_second_request_response,
        ],
    )

    # Call the function to test
    schedule, instructorid_map = get_zingfit_schedule_and_instructorid_map(
        logger=mock_logger,
        studio_name="test studio",
        studio_url_subdomain=ABSOLUTE_URL_SUBDOMAIN,
        table_heading_date_format=ABSOLUTE_TABLE_HEADING_DATE_FORMAT,
        max_weeks=ABSOLUTE_MAX_WEEKS,
        location_to_site_id_map=ABSOLUTE_LOCATION_TO_SITE_ID_MAP,
        room_id_to_studio_type_map=ABSOLUTE_ROOM_ID_TO_STUDIO_TYPE_MAP,
        room_id_to_studio_location_map=ABSOLUTE_ROOM_ID_TO_STUDIO_LOCATION_MAP,
        clean_class_name_func=None,
    )

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == absolute_expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == absolute_expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_SCHEDULE[key], (
            f"Expected result list {absolute_expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_SCHEDULE[key]} "
            f"does not match actual result list {schedule.classes[key]}."
        )
    assert instructorid_map == absolute_expected_results.EXPECTED_CTP_AND_GW_7_TO_20_APR_INSTRUCTORID_MAP


def test_get_zingfit_schedule_and_instructorid_map_ally_flow(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_ally_schedule_and_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_week_0_request_response = mocker.Mock()
    mock_week_0_request_response.text = load_response_file("ally_crossstreet_8_to_14_apr.html")

    mock_week_1_request_response = mocker.Mock()
    mock_week_1_request_response.text = load_response_file("ally_crossstreet_15_to_21_apr.html")

    mock_week_2_request_response = mocker.Mock()
    mock_week_2_request_response.text = load_response_file("ally_crossstreet_22_to_28_apr.html")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_week_0_request_response,
            mock_week_1_request_response,
            mock_week_2_request_response,
        ],
    )

    # Call the function to test
    schedule, instructorid_map = get_zingfit_schedule_and_instructorid_map(
        logger=mock_logger,
        studio_name="test studio",
        studio_url_subdomain=ALLY_URL_SUBDOMAIN,
        table_heading_date_format=ALLY_TABLE_HEADING_DATE_FORMAT,
        max_weeks=ALLY_MAX_WEEKS,
        location_to_site_id_map=ALLY_LOCATION_TO_SITE_ID_MAP,
        room_id_to_studio_type_map=ALLY_ROOM_ID_TO_STUDIO_TYPE_MAP,
        room_id_to_studio_location_map=ALLY_ROOM_ID_TO_STUDIO_LOCATION_MAP,
        clean_class_name_func=ally_clean_class_name_func,
    )

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == ally_expected_results.EXPECTED_CROSSSTREET_8_TO_28_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == ally_expected_results.EXPECTED_CROSSSTREET_8_TO_28_APR_SCHEDULE[key], (
            f"Expected result list {ally_expected_results.EXPECTED_CROSSSTREET_8_TO_28_APR_SCHEDULE[key]} "
            f"does not match actual result list {schedule.classes[key]}."
        )
    assert instructorid_map == ally_expected_results.EXPECTED_CROSSSTREET_8_TO_28_APR_INSTRUCTORID_MAP
