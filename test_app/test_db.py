from typing import Generator
from unittest.mock import MagicMock, patch

from peewee import SqliteDatabase

from app.source.models import Driver, models
from db.fill_db import RaceData, infill_drivers_db
from test_app.utilities import create_test_driver


def test_create_db_tables(tables: SqliteDatabase) -> None:
    for driver in models:
        assert tables.table_exists(driver)


@patch("db.fill_db.RaceData")
def test_infill_drivers_db(race_data_mock: MagicMock, data: RaceData, tables: Generator) -> None:
    drivers_quantity = 3
    instance = race_data_mock.return_value
    instance.analyzer.drivers_race_data = [create_test_driver(counter + 1) for counter in range(drivers_quantity)]
    infill_drivers_db("test path")
    data = Driver.select()

    for count, driver in enumerate(data, start=1):
        assert [driver.abbreviation, driver.full_name, driver.team, driver.lap_time] == [
            f"Driver_{count}",
            f"Test driver #{count}",
            f"Test team #{count}",
            f"Test lap time #{count}",
        ]
