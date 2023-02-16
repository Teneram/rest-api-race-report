import racing_report

from app.source.models import Driver
from db.logger import logging

fill_tables_logger = logging.getLogger(__name__)


class RaceData:
    def __init__(self, path: str) -> None:
        fill_tables_logger.info("Race data initializing started")
        self.analyzer = racing_report.RacingDataAnalyzer(path)
        self.analyzer.build_report()
        fill_tables_logger.info("Race data initializing succeeded")


def infill_drivers_db(data_path: str) -> None:
    fill_tables_logger.info("Inserting data to database started")
    data = RaceData(data_path)
    drivers_data = []
    for driver in data.analyzer.drivers_race_data:
        driver_data = {
            "abbreviation": driver.abbreviation,
            "full_name": driver.full_name,
            "team": driver.team,
            "lap_time": (None if driver.lap_time == "Invalid lap time" else driver.lap_time),
        }
        drivers_data.append(driver_data)
        fill_tables_logger.info(f"Driver data {driver_data} initialized".encode(encoding="UTF-8"))
    Driver.insert_many(drivers_data).execute()
    fill_tables_logger.info("Adding drivers data to database succeeded")
