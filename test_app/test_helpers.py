from http import HTTPStatus
from typing import Generator

import pytest
import xmltodict

from app.source.helpers import serialize_response
from constants import FormatEnum


@pytest.mark.parametrize(
    "data_format, expected_result",
    [
        (
            FormatEnum.xml,
            {"report": {"driver_id": "id", "full_name": "name", "lap_time_": "time"}},
        ),
        (FormatEnum.json, b'{"driver_id":"id","full_name":"name","lap_time>":"time"}\n'),
        (FormatEnum.none, b'{"driver_id":"id","full_name":"name","lap_time>":"time"}\n'),
    ],
)
def test_serialize_response(app_context: Generator, data_format: FormatEnum, expected_result: str) -> None:
    response = serialize_response(data_format, {"driver_id": "id", "full_name": "name", "lap_time>": "time"})

    if data_format == FormatEnum.xml:
        assert xmltodict.parse(response.data) == expected_result
    else:
        assert response.data == expected_result
    assert response.status_code == HTTPStatus.OK
