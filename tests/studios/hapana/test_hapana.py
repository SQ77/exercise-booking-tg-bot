"""
test_hapana.py
Author: https://github.com/lendrixxx
Description: This file tests the functions to retrieve information for Hapana.
"""

import json
import logging
from datetime import date, datetime
from typing import Callable, NamedTuple

import pytest
import pytest_mock
import requests

from common.capacity_info import CapacityInfo
from common.class_availability import ClassAvailability
from common.class_data import ClassData
from common.result_data import ResultData
from common.studio_location import StudioLocation
from common.studio_type import StudioType
from studios.hapana.data.rev import LOCATION_TO_SITE_ID_MAP as REV_LOCATION_TO_SITE_ID_MAP
from studios.hapana.data.rev import ROOM_ID_TO_STUDIO_TYPE_MAP as REV_ROOM_ID_TO_STUDIO_TYPE_MAP
from studios.hapana.data.rev import ROOM_NAME_TO_STUDIO_LOCATION_MAP as REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP
from studios.hapana.hapana import (
    get_hapana_schedule,
    get_hapana_schedule_and_instructorid_map,
    get_hapana_security_token,
    get_instructorid_map,
    parse_get_schedule_response,
    send_get_schedule_request,
)
from tests.studios.hapana.expected_results import rev_expected_results


def test_get_hapana_security_token_success(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_hapana_security_token success flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    expected_security_token = "test_security_token"

    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = json.dumps({"securityToken": expected_security_token})

    # Call the function to test
    site_id = "test_site_id"
    security_token = get_hapana_security_token(
        logger=mock_logger,
        studio_name="test studio",
        site_id=site_id,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/settings",
        headers={"wID": site_id},
    )
    assert security_token == expected_security_token


def test_get_hapana_security_token_api_failure(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_hapana_security_token API failure flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 500

    # Call the function to test
    site_id = "test_site_id"
    security_token = get_hapana_security_token(
        logger=mock_logger,
        studio_name="test studio",
        site_id=site_id,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/settings",
        headers={"wID": site_id},
    )
    assert security_token == ""


def test_get_hapana_security_token_parse_json_failure(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_hapana_security_token parse json failure flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "not_a_json"

    # Call the function to test
    site_id = "test_site_id"
    security_token = get_hapana_security_token(
        logger=mock_logger,
        studio_name="test studio",
        site_id=site_id,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/settings",
        headers={"wID": site_id},
    )
    assert security_token == ""


def test_get_hapana_security_token_response_failure(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test get_hapana_security_token security token not in response failure flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = json.dumps({"no_security_token": "test"})

    # Call the function to test
    site_id = "test_site_id"
    security_token = get_hapana_security_token(
        logger=mock_logger,
        studio_name="test studio",
        site_id=site_id,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/settings",
        headers={"wID": site_id},
    )
    assert security_token == ""


def test_send_get_schedule_request(mocker: pytest_mock.plugin.MockerFixture) -> None:
    """
    Test send_get_schedule_request flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.

    """
    # Setup mocks
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200

    # Call the function to test
    location = StudioLocation.Bugis
    start_date = date(2025, 4, 8)
    end_date = date(2025, 4, 29)
    security_token = "test_security_token"
    response = send_get_schedule_request(
        location=location,
        start_date=start_date,
        end_date=end_date,
        security_token=security_token,
        location_to_site_id_map=REV_LOCATION_TO_SITE_ID_MAP,
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/sessions",
        params={
            "sessionCategory": "classes",
            "siteID": REV_LOCATION_TO_SITE_ID_MAP[location],
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
        },
        headers={
            "Content-Type": "application/json",
            "Securitytoken": security_token,
        },
    )
    assert response.status_code == 200


def test_parse_get_schedule_response_success(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test parse_get_schedule_response flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.status_code = 200
    mock_response.text = load_response_file("rev_orchard_9_to_18_apr.json")

    # Call the function to test
    result = parse_get_schedule_response(
        logger=mock_logger,
        studio_name="test studio",
        response=mock_response,
        room_id_to_studio_type_map=REV_ROOM_ID_TO_STUDIO_TYPE_MAP,
        room_name_to_studio_location_map=REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP,
    )

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == rev_expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE.keys()
    for key in result:
        assert result[key] == rev_expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE[key], (
            f"Expected result list does not match actual result list\n"
            f"Expected: {rev_expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE[key]}\n"
            f"Actual: {result[key]}"
        )

        for index, actual_class_data in enumerate(result[key]):
            expected_class_data = rev_expected_results.EXPECTED_ORCHARD_9_TO_18_APR_SCHEDULE[key][index]
            assert actual_class_data.availability == expected_class_data.availability, (
                f"Expected class availability does not match actual availability\n"
                f"Expected: {expected_class_data.availability}\n"
                f"Actual: {actual_class_data.availability}"
            )
            assert actual_class_data.capacity_info == expected_class_data.capacity_info, (
                f"Expected class capacity info does not match actual capacity info\n"
                f"Expected: {expected_class_data.capacity_info}\n"
                f"Actual: {actual_class_data.capacity_info}"
            )


class ParseGetScheduleResponseFailureArgs(NamedTuple):
    expected_response_status_code: int
    expected_response_json_str: str
    expected_result_dict: dict[date, list[ClassData]]
    expected_warning_logs: list[str]


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            ParseGetScheduleResponseFailureArgs(
                expected_response_status_code=400,
                expected_response_json_str="",
                expected_result_dict={},
                expected_warning_logs=["Failed to get test studio schedule - API callback error 400"],
            ),
            id="API callback error",
        ),
        pytest.param(
            ParseGetScheduleResponseFailureArgs(
                expected_response_status_code=200,
                expected_response_json_str=json.dumps({"no-success": False}),
                expected_result_dict={},
                expected_warning_logs=[
                    "Failed to get test studio schedule - API callback failed: {'no-success': False}",
                ],
            ),
            id="API callback failed",
        ),
        pytest.param(
            ParseGetScheduleResponseFailureArgs(
                expected_response_status_code=200,
                expected_response_json_str="abc",
                expected_result_dict={},
                expected_warning_logs=[
                    "Failed to get test studio schedule - Expecting value: line 1 column 1 (char 0): abc",
                ],
            ),
            id="Response JSON parsing failed",
        ),
        pytest.param(
            ParseGetScheduleResponseFailureArgs(
                expected_response_status_code=200,
                expected_response_json_str=json.dumps(
                    {
                        "success": True,
                        "data": [
                            {
                                "sessionStatus": "open",
                                "sessionDate": "2025-04-10",
                                "startTime": "13:15:00",
                                "instructorData": [
                                    {
                                        "instructorID": "test_instructor_id",
                                        "instructorName": "rev instructor",
                                    }
                                ],
                                "sessionName": "test class name @ bugis",
                                "roomName": "unknown room",
                                "capacity": 20,
                                "remaining": 5,
                                "waitlistCapacity": 20,
                                "waitlistReserved": 0,
                            },
                        ],
                    }
                ),
                expected_result_dict={
                    datetime.strptime("2025-04-10", "%Y-%m-%d").date(): [
                        ClassData(
                            studio=StudioType.Unknown,
                            location=StudioLocation.Unknown,
                            name="test class name @ unknown room",
                            instructor="rev instructor",
                            time="1:15 PM",
                            availability=ClassAvailability.Available,
                            capacity_info=CapacityInfo(
                                has_info=True,
                                capacity=20,
                                remaining=5,
                                waitlist_capacity=20,
                                waitlist_reserved=0,
                            ),
                        )
                    ]
                },
                expected_warning_logs=[
                    "Failed to map room name unknown room to studio type for test studio",
                    "Failed to map room name unknown room to studio location for test studio",
                ],
            ),
            id="Unknown room name",
        ),
        pytest.param(
            ParseGetScheduleResponseFailureArgs(
                expected_response_status_code=200,
                expected_response_json_str=json.dumps({"success": True, "data": {"not-list": 123}}),
                expected_result_dict={},
                expected_warning_logs=[
                    "Failed to get details of class for test studio - string indices must be integers. Data: not-list",
                ],
            ),
            id="Exception when parsing data",
        ),
    ],
)
def test_parse_get_schedule_response_failure(
    mocker: pytest_mock.plugin.MockerFixture,
    args: ParseGetScheduleResponseFailureArgs,
) -> None:
    """
    Test parse_get_schedule_response failure flows.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (ParseGetScheduleResponseFailureArgs): Provides arguments for the test case.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock(spec=requests.models.Response)
    mock_response.status_code = args.expected_response_status_code
    mock_response.text = args.expected_response_json_str

    # Call the function to test
    result = parse_get_schedule_response(
        logger=mock_logger,
        studio_name="test studio",
        response=mock_response,
        room_id_to_studio_type_map=REV_ROOM_ID_TO_STUDIO_TYPE_MAP,
        room_name_to_studio_location_map=REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP,
    )

    # Assert that flow was called with the expected arguments
    expected_warning_calls = []
    for expected_warning_log in args.expected_warning_logs:
        expected_warning_calls.append(mocker.call(expected_warning_log))
    assert mock_logger.warning.call_args_list == expected_warning_calls

    # Assert that the response is as expected
    assert isinstance(result, dict)
    assert result.keys() == args.expected_result_dict.keys()
    for key in result:
        assert result[key] == args.expected_result_dict[key], (
            f"Expected result list does not match actual result list\n"
            f"Expected: {args.expected_result_dict[key]}\n"
            f"Actual: {result[key]}"
        )

        for index, actual_class_data in enumerate(result[key]):
            expected_class_data = args.expected_result_dict[key][index]
            assert actual_class_data.availability == expected_class_data.availability, (
                f"Expected class availability does not match actual availability\n"
                f"Expected: {expected_class_data.availability}\n"
                f"Actual: {actual_class_data.availability}"
            )
            assert actual_class_data.capacity_info == expected_class_data.capacity_info, (
                f"Expected class capacity info does not match actual capacity info\n"
                f"Expected: {expected_class_data.capacity_info}\n"
                f"Actual: {actual_class_data.capacity_info}"
            )


def test_get_hapana_schedule(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_hapana_schedule flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_bugis_schedule_request_response = mocker.Mock()
    mock_bugis_schedule_request_response.status_code = 200
    mock_bugis_schedule_request_response.text = load_response_file("rev_bugis_10_to_12_apr.json")

    mock_orchard_schedule_request_response = mocker.Mock()
    mock_orchard_schedule_request_response.status_code = 200
    mock_orchard_schedule_request_response.text = load_response_file("rev_orchard_10_to_12_apr.json")

    mock_tjpg_schedule_request_response = mocker.Mock()
    mock_tjpg_schedule_request_response.status_code = 200
    mock_tjpg_schedule_request_response.text = load_response_file("rev_tjpg_10_to_12_apr.json")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_bugis_schedule_request_response,
            mock_orchard_schedule_request_response,
            mock_tjpg_schedule_request_response,
        ],
    )

    # Call the function to test
    schedule = get_hapana_schedule(
        logger=mock_logger,
        studio_name="test studio",
        security_token="test_security_token",
        location_to_site_id_map=REV_LOCATION_TO_SITE_ID_MAP,
        room_id_to_studio_type_map=REV_ROOM_ID_TO_STUDIO_TYPE_MAP,
        room_name_to_studio_location_map=REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP,
    )

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key], (
            f"Expected result list does not match actual result list\n"
            f"Expected: {rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key]}\n"
            f"Actual: {schedule.classes[key]}"
        )

        for index, actual_class_data in enumerate(schedule.classes[key]):
            expected_class_data = rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key][index]
            assert actual_class_data.availability == expected_class_data.availability, (
                f"Expected class availability does not match actual availability\n"
                f"Expected: {expected_class_data.availability}\n"
                f"Actual: {actual_class_data.availability}"
            )
            assert actual_class_data.capacity_info == expected_class_data.capacity_info, (
                f"Expected class capacity info does not match actual capacity info\n"
                f"Expected: {expected_class_data.capacity_info}\n"
                f"Actual: {actual_class_data.capacity_info}"
            )


def test_get_instructorid_map(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_bugis_instructors_request_response = mocker.Mock()
    mock_bugis_instructors_request_response.status_code = 200
    mock_bugis_instructors_request_response.text = load_response_file("rev_bugis_instructors.json")

    mock_orchard_instructors_request_response = mocker.Mock()
    mock_orchard_instructors_request_response.status_code = 200
    mock_orchard_instructors_request_response.text = load_response_file("rev_orchard_instructors.json")

    mock_tjpg_instructors_request_response = mocker.Mock()
    mock_tjpg_instructors_request_response.status_code = 200
    mock_tjpg_instructors_request_response.text = load_response_file("rev_tjpg_instructors.json")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_bugis_instructors_request_response,
            mock_orchard_instructors_request_response,
            mock_tjpg_instructors_request_response,
        ],
    )

    # Call the function to test
    instructorid_map = get_instructorid_map(
        logger=mock_logger,
        studio_name="test studio",
        security_token="test_security_token",
        location_to_site_id_map=REV_LOCATION_TO_SITE_ID_MAP,
    )

    # Assert that the response is as expected
    assert instructorid_map == rev_expected_results.EXPECTED_BUGIS_10_TO_12_APR_INSTRUCTORID_MAP


class GetInstructorIDMapFailureArgs(NamedTuple):
    expected_response_status_code: int
    expected_response_json_str: str
    expected_instructorid_map: dict[str, str]
    expected_warning_log: str


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(
            GetInstructorIDMapFailureArgs(
                expected_response_status_code=400,
                expected_response_json_str="",
                expected_instructorid_map={},
                expected_warning_log=str(
                    "Failed to get test studio list of instructors for test_location - API callback error 400"
                ),
            ),
            id="API callback error",
        ),
        pytest.param(
            GetInstructorIDMapFailureArgs(
                expected_response_status_code=200,
                expected_response_json_str=json.dumps({"success": False}),
                expected_instructorid_map={},
                expected_warning_log="Failed to get test studio list of instructors for test_location - "
                "API callback failed: {'success': False}",
            ),
            id="API callback failed",
        ),
        pytest.param(
            GetInstructorIDMapFailureArgs(
                expected_response_status_code=200,
                expected_response_json_str=json.dumps({"no-success": 123}),
                expected_instructorid_map={},
                expected_warning_log="Failed to get test studio list of instructors for test_location - 'success'",
            ),
            id="Response JSON parsing failed",
        ),
    ],
)
def test_get_instructorid_map_failure(
    mocker: pytest_mock.plugin.MockerFixture,
    args: GetInstructorIDMapFailureArgs,
) -> None:
    """
    Test get_instructorid_map failure flows.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - args (GetInstructorIDMapFailureArgs): Provides arguments for the test case.

    """
    security_token = "test_security_token"

    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_response = mocker.Mock()
    mock_response.status_code = args.expected_response_status_code
    mock_response.text = args.expected_response_json_str

    mock_get = mocker.patch("requests.get", return_value=mock_response)

    # Call the function to test
    instructorid_map = get_instructorid_map(
        logger=mock_logger,
        studio_name="test studio",
        security_token=security_token,
        location_to_site_id_map={"test_location": 1},
    )

    # Assert that flow was called with the expected arguments
    mock_get.assert_called_once_with(
        url="https://widgetapi.hapana.com/v2/wAPI/site/instructor",
        headers={
            "Content-Type": "application/json",
            "Securitytoken": security_token,
        },
        params={
            "siteID": 1,
        },
    )
    mock_logger.warning.assert_called_once_with(args.expected_warning_log)

    # Assert that the response is as expected
    assert instructorid_map == args.expected_instructorid_map


def test_get_hapana_schedule_and_instructorid_map(
    mocker: pytest_mock.plugin.MockerFixture, load_response_file: Callable[[str], str]
) -> None:
    """
    Test get_hapana_schedule_and_instructorid_map flow.

    Args:
      - mocker (pytest_mock.plugin.MockerFixture): Provides mocking utilities for patching and mocking.
      - load_response_file (Callable[[str], str]): Fixture that loads file content from the example_responses folder.

    """
    # Setup mocks
    mock_logger = mocker.Mock(spec=logging.Logger)

    mock_bugis_schedule_request_response = mocker.Mock()
    mock_bugis_schedule_request_response.status_code = 200
    mock_bugis_schedule_request_response.text = load_response_file("rev_bugis_10_to_12_apr.json")

    mock_orchard_schedule_request_response = mocker.Mock()
    mock_orchard_schedule_request_response.status_code = 200
    mock_orchard_schedule_request_response.text = load_response_file("rev_orchard_10_to_12_apr.json")

    mock_tjpg_schedule_request_response = mocker.Mock()
    mock_tjpg_schedule_request_response.status_code = 200
    mock_tjpg_schedule_request_response.text = load_response_file("rev_tjpg_10_to_12_apr.json")

    mock_bugis_instructors_request_response = mocker.Mock()
    mock_bugis_instructors_request_response.status_code = 200
    mock_bugis_instructors_request_response.text = load_response_file("rev_bugis_instructors.json")

    mock_orchard_instructors_request_response = mocker.Mock()
    mock_orchard_instructors_request_response.status_code = 200
    mock_orchard_instructors_request_response.text = load_response_file("rev_orchard_instructors.json")

    mock_tjpg_instructors_request_response = mocker.Mock()
    mock_tjpg_instructors_request_response.status_code = 200
    mock_tjpg_instructors_request_response.text = load_response_file("rev_tjpg_instructors.json")

    mocker.patch(
        "requests.get",
        side_effect=[
            mock_bugis_schedule_request_response,
            mock_orchard_schedule_request_response,
            mock_tjpg_schedule_request_response,
            mock_bugis_instructors_request_response,
            mock_orchard_instructors_request_response,
            mock_tjpg_instructors_request_response,
        ],
    )

    # Call the function to test
    schedule, instructorid_map = get_hapana_schedule_and_instructorid_map(
        logger=mock_logger,
        studio_name="test studio",
        security_token="test_security_token",
        location_to_site_id_map=REV_LOCATION_TO_SITE_ID_MAP,
        room_id_to_studio_type_map=REV_ROOM_ID_TO_STUDIO_TYPE_MAP,
        room_name_to_studio_location_map=REV_ROOM_NAME_TO_STUDIO_LOCATION_MAP,
    )

    # Assert that the response is as expected
    assert isinstance(schedule, ResultData)
    assert isinstance(schedule.classes, dict)
    assert schedule.classes.keys() == rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE.keys()
    for key in schedule.classes:
        assert schedule.classes[key] == rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key], (
            f"Expected result list does not match actual result list\n"
            f"Expected: {rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key]}\n"
            f"Actual: {schedule.classes[key]}"
        )

        for index, actual_class_data in enumerate(schedule.classes[key]):
            expected_class_data = rev_expected_results.EXPECTED_ALL_10_TO_12_APR_SCHEDULE[key][index]
            assert actual_class_data.availability == expected_class_data.availability, (
                f"Expected class availability does not match actual availability\n"
                f"Expected: {expected_class_data.availability}\n"
                f"Actual: {actual_class_data.availability}"
            )
            assert actual_class_data.capacity_info == expected_class_data.capacity_info, (
                f"Expected class capacity info does not match actual capacity info\n"
                f"Expected: {expected_class_data.capacity_info}\n"
                f"Actual: {actual_class_data.capacity_info}"
            )
    assert instructorid_map == rev_expected_results.EXPECTED_BUGIS_10_TO_12_APR_INSTRUCTORID_MAP
