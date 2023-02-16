from dataclasses import asdict
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from racing_report import Driver as My_driver

from app.source.manager import RaceManager
from app.source.models import Driver
from constants import OrderEnum
from db.fill_db import RaceData
from test_app.utilities import create_drivers_data, create_test_driver


class TestRaceDB:
    @pytest.mark.parametrize("order", [OrderEnum.asc, OrderEnum.desc])
    def test_sort_data(self, order: OrderEnum) -> None:
        direction = True if order == OrderEnum.desc else False
        expected_result = Driver.select().order_by(
            Driver.lap_time.desc(nulls="LAST") if direction else Driver.lap_time.asc(nulls="LAST")
        )
        assert RaceManager.sort_data(order) == expected_result

    @patch("db.fill_db.RaceData")
    def test_create_report_data(self, race_data_mock: MagicMock, data: RaceData, tables: Generator) -> None:
        drivers_quantity = 3
        instance = race_data_mock.return_value
        instance.analyzer.drivers_race_data = "mocked values"
        data.analyzer.drivers_race_data = [create_test_driver(counter + 1) for counter in range(drivers_quantity)]
        drivers_data = create_drivers_data(data.analyzer.drivers_race_data)

        Driver.insert_many(drivers_data).execute()
        data = Driver.select()

        expected_result = {
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

        assert RaceManager.create_report_data(data) == expected_result

    @patch("db.fill_db.RaceData")
    def test_create_drivers_info(self, race_data_mock: MagicMock, data: RaceData, tables: Generator) -> None:
        drivers_quantity = 3
        instance = race_data_mock.return_value
        instance.analyzer.drivers_race_data = "mocked values"
        data.analyzer.drivers_race_data = [create_test_driver(counter + 1) for counter in range(drivers_quantity)]
        drivers_data = create_drivers_data(data.analyzer.drivers_race_data)

        Driver.insert_many(drivers_data).execute()
        data = Driver.select()

        expected_result = {
            "data": [
                {"abbreviation": f"Driver_{number}", "full_name": f"Test driver #{number}"}
                for number in range(1, drivers_quantity + 1)
            ]
        }

        assert RaceManager.create_drivers_info(data) == expected_result

    @pytest.mark.parametrize(
        "driver_id, expected_result",
        (
            [
                "Driver_1",
                asdict(
                    My_driver(
                        abbreviation="Driver_1",
                        full_name="Test driver #1",
                        team="Test team #1",
                        lap_time="Test lap time #1",
                    )
                ),
            ],
            ["Driver_3", None],
        ),
    )
    @patch("db.fill_db.RaceData")
    def test_get_driver(
        self, race_data_mock: MagicMock, data: RaceData, driver_id: str, expected_result: My_driver, tables: Generator
    ) -> None:
        drivers_quantity = 2
        instance = race_data_mock.return_value
        instance.analyzer.drivers_race_data = "mocked values"
        data.analyzer.drivers_race_data = [create_test_driver(counter + 1) for counter in range(drivers_quantity)]
        drivers_data = create_drivers_data(data.analyzer.drivers_race_data)

        Driver.insert_many(drivers_data).execute()

        assert RaceManager.get_driver(driver_id) == expected_result
