from racing_report import Driver

from test_app.utilities import create_drivers_data, create_test_driver


def test_create_test_driver() -> None:
    expected_result = Driver(
        abbreviation="Driver_1", full_name="Test driver #1", team="Test team #1", lap_time="Test lap time #1"
    )
    assert create_test_driver(1) == expected_result


def test_create_drivers_data() -> None:
    drivers_quantity = 2
    data_input = [
        Driver(
            abbreviation=f"Driver_{number}",
            full_name=f"Test driver #{number}",
            team=f"Test team #{number}",
            lap_time=f"Test lap time #{number}",
        )
        for number in range(1, drivers_quantity + 1)
    ]
    expected_result = [
        {
            "abbreviation": f"Driver_{number}",
            "full_name": f"Test driver #{number}",
            "team": f"Test team #{number}",
            "lap_time": f"Test lap time #{number}",
        }
        for number in range(1, drivers_quantity + 1)
    ]
    assert create_drivers_data(data_input) == expected_result
