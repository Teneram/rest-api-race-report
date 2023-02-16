from http import HTTPStatus

from flask import abort


def database_error(error):
    abort(HTTPStatus.BAD_GATEWAY, "There is no appropriate database")


def server_error(error):
    abort(HTTPStatus.NOT_FOUND, "The requested page was not found")
