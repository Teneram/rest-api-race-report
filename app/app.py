from http import HTTPStatus

from flasgger import Swagger
from flask import Flask
from flask_restful import Api
from peewee import OperationalError

from app.source.errors import database_error, server_error
from constants import VERSION

app = Flask(__name__)
app.register_error_handler(OperationalError, database_error)
app.register_error_handler(HTTPStatus.INTERNAL_SERVER_ERROR, server_error)
swagger = Swagger(app)
api = Api(app)

from app.source.views import DriversDetails, DriversInformation, Report  # noqa

api.add_resource(Report, f"/api/v{VERSION}/report")
api.add_resource(DriversInformation, f"/api/v{VERSION}/report/drivers")
api.add_resource(DriversDetails, f"/api/v{VERSION}/report/drivers/<driver_id>")
