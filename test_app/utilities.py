from typing import Any, Dict, List

from racing_report import Driver


def create_test_driver(number: int) -> Driver:
    return Driver(
        abbreviation=f"Driver_{number}",
        full_name=f"Test driver #{number}",
        team=f"Test team #{number}",
        lap_time=f"Test lap time #{number}",
    )


def create_drivers_data(data: List[Driver]) -> List[Dict[str, Any | None]]:
    drivers_data = []
    for driver in data:
        driver_data = {
            "abbreviation": driver.abbreviation,
            "full_name": driver.full_name,
            "team": driver.team,
            "lap_time": (None if driver.lap_time == "Invalid lap time" else driver.lap_time),
        }
        drivers_data.append(driver_data)
    return drivers_data
