from dataclasses import asdict
from http import HTTPStatus
from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

import pytest
from flask.testing import FlaskClient

from constants import FormatEnum, OrderEnum
from test_app.utilities import create_test_driver


class TestReport:

    url = "/api/v1/report"

    @pytest.mark.parametrize("order", [OrderEnum.asc, OrderEnum.desc])
    @patch("app.source.manager.RaceManager.create_report_data")
    def test_index_data(self, create_report_data_mock: MagicMock, order: FormatEnum, client: FlaskClient) -> None:
        drivers_quantity = 1
        create_report_data_mock.return_value = {
            "data": [
                {
                    "position": number,
                    "driver_info": {
                        "full_name": f"Test driver #{number}",
                        "team": f"Test team #{number}",
                        "lap_time": f"Test lap time #{number}",
                    },
                }
                for number in range(1, drivers_quantity + 1)
            ]
        }

        expected_result = (
            b'{\n  "data": [\n    {\n      "driver_info": {\n        "full_name": "Test driver #1",'
            b'\n        "lap_time": "Test lap time #1",\n        "team": "Test team #1"\n      },'
            b'\n      "position": 1\n    }\n  ]\n}\n'
        )

        response = client.get(urljoin(self.url, f"?order={order.name}"))

        assert expected_result == response.data
        assert response.status_code == HTTPStatus.OK
        assert response.content_type == "application/json"

        create_report_data_mock.assert_called()

    @pytest.mark.parametrize("form", [FormatEnum.json, FormatEnum.xml])
    @patch("app.source.views.RaceManager")
    def test_index_query(self, race_data_mock: MagicMock, form: FormatEnum, client: FlaskClient) -> None:
        instance = race_data_mock.return_value
        instance.analyzer.drivers_race_data = [create_test_driver(counter + 1) for counter in range(2)]

        response = client.get(urljoin(self.url, f"?format={form.name}&order=asc"))

        assert response.content_type == f"application/{form.name}"
        race_data_mock.sort_data.assert_called_with(OrderEnum.asc)


class TestDriversInformation:
    url = "/api/v1/report/drivers"

    @pytest.mark.parametrize("order", [OrderEnum.asc, OrderEnum.desc])
    @patch("app.source.manager.RaceManager.create_drivers_info")
    def test_index_data(self, create_drivers_info_mock: MagicMock, order: OrderEnum, client: FlaskClient) -> None:
        drivers_quantity = 1
        create_drivers_info_mock.return_value = {
            "data": [
                {"abbreviation": f"Driver_{number}", "full_name": f"Test driver #{number}"}
                for number in range(1, drivers_quantity + 1)
            ]
        }

        expected_result = (
            b'{\n  "data": [\n    {\n      "abbreviation": "Driver_1",\n      '
            b'"full_name": "Test driver #1"\n    }\n  ]\n}\n'
        )
        response = client.get(urljoin(self.url, f"?order={order.name}"))

        assert expected_result == response.data
        assert response.status_code == HTTPStatus.OK
        assert response.content_type == "application/json"

        create_drivers_info_mock.assert_called()

    @pytest.mark.parametrize("form", [FormatEnum.json, FormatEnum.xml])
    @pytest.mark.parametrize("order", [OrderEnum.asc, OrderEnum.desc])
    @patch("app.source.views.RaceManager")
    def test_index_query(
        self, race_data_mock: MagicMock, form: FormatEnum, order: OrderEnum, client: FlaskClient
    ) -> None:
        instance = race_data_mock.return_value
        instance.analyzer.drivers_race_data = [create_test_driver(counter + 1) for counter in range(2)]

        response = client.get(urljoin(self.url, f"?format={form.name}&order={order.name}"))

        assert response.content_type == f"application/{form.name}"
        race_data_mock.sort_data.assert_called_with(order)


class TestDriverDetails:
    url = "/api/v1/report/drivers/"

    @patch("app.source.views.RaceManager.get_driver")
    def test_driver_details_data_valid(self, get_driver_mock: MagicMock, client: FlaskClient) -> None:
        test_driver = "Driver_1"
        get_driver_mock.return_value = asdict(create_test_driver(1))
        expected_result = {
            "abbreviation": f"{test_driver}",
            "full_name": "Test driver #1",
            "team": "Test team #1",
            "lap_time": "Test lap time #1",
        }

        response = client.get(urljoin(self.url, test_driver))

        assert expected_result == response.json
        assert response.status_code == HTTPStatus.OK

        get_driver_mock.assert_called_with(test_driver)

    @patch("app.source.views.RaceManager.get_driver")
    def test_driver_details_data_invalid(self, get_driver_mock: MagicMock, client: FlaskClient) -> None:
        test_driver = "Invalid driver"
        get_driver_mock.return_value = None

        response = client.get(urljoin(self.url, test_driver))

        assert response.status_code == HTTPStatus.NOT_FOUND

        get_driver_mock.assert_called_with(test_driver)

    @pytest.mark.parametrize("form", [FormatEnum.json.name, FormatEnum.xml.name])
    @patch("app.source.views.RaceManager.get_driver")
    def test_driver_details_query(self, get_driver_mock: MagicMock, form: str, client: FlaskClient) -> None:
        get_driver_mock.return_value = asdict(create_test_driver(1))

        response = client.get(urljoin(self.url, f"Driver_1?format={form}"))

        assert response.content_type == f"application/{form}"
