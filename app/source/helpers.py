from http import HTTPStatus

from dict2xml import dict2xml
from flask import make_response
from flask.wrappers import Response

from constants import ROOT_NAME, FormatEnum


def serialize_response(response_type: FormatEnum, data: dict) -> Response:
    if response_type == FormatEnum.xml:
        new_data = {ROOT_NAME: data}
        data = dict2xml(new_data)
    else:
        response_type = FormatEnum.json
    response = make_response(data, HTTPStatus.OK)
    response.headers["Content-Type"] = f"application/{response_type.name}"
    return response
