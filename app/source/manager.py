from typing import Any, Dict, List

from peewee import DoesNotExist, ModelSelect

from app.source.models import Driver
from constants import OrderEnum


class RaceManager:
    @staticmethod
    def sort_data(order: OrderEnum) -> ModelSelect:
        direction = True if order == OrderEnum.desc else False
        drivers_data = Driver.select().order_by(
            Driver.lap_time.desc(nulls="LAST") if direction else Driver.lap_time.asc(nulls="LAST")
        )
        return drivers_data

    @staticmethod
    def create_report_data(drivers_data: ModelSelect) -> Dict[str, List[Dict[str, Any]]] | Dict[str, str]:
        report_data: Dict[str, List[Dict[str, Any]]] = {"data": []}
        for count, driver in enumerate(drivers_data, 1):
            statistic = {
                "position": count,
                "driver_info": {"full_name": driver.full_name, "team": driver.team, "lap_time": driver.lap_time},
            }
            report_data["data"].append(statistic)
        return report_data

    @staticmethod
    def create_drivers_info(drivers_data: ModelSelect) -> Dict[str, List[Dict[str, str]]] | Dict[str, str]:
        drivers_info_data = {
            "data": [{"full_name": driver.full_name, "abbreviation": driver.abbreviation} for driver in drivers_data]
        }
        return drivers_info_data

    @staticmethod
    def get_driver(driver_id: str) -> Dict[str, str] | None:
        try:
            driver = Driver.get(Driver.abbreviation == driver_id)
            return {
                "abbreviation": driver.abbreviation,
                "full_name": driver.full_name,
                "lap_time": driver.lap_time,
                "team": driver.team,
            }
        except DoesNotExist:
            return None
