from http import HTTPStatus

from flask import abort, request
from flask.wrappers import Response
from flask_restful import Resource

from app.source.helpers import serialize_response
from app.source.manager import RaceManager
from constants import FormatEnum, OrderEnum


class Report(Resource):
    def get(self) -> Response:
        """Sorted report of driver's results
        ---
        definitions:
          MyData:
            type: object
            properties:
              data:
                type: array
                items:
                    type: object
                    properties:
                        position:
                            type: integer
                            example: 1
                        driver_info:
                            type: object
                            properties:
                                full_name:
                                    type: string
                                    example: Sebastian Vettel
                                team:
                                    type: string
                                    example: FERRARI
                                lap_time:
                                    type: string
                                    example: "01:04.415"
          NoContent:
            type: object
            properties:
                massage:
                    type: string
                    example: There is no appropriate database
        parameters:
          - name: order
            in: query
            type: string
            enum: ['asc', 'desc']
            required: false
            default: asc
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            required: false
            default: json
        responses:
          200:
            description: Report of driver's results
            schema:
              $ref: '#/definitions/MyData'
          502:
            description: Particular driver statistic
            schema:
              $ref: '#/definitions/NoContent'
        """
        args = request.args
        sorted_data = RaceManager.sort_data(OrderEnum(args.get("order")))
        report_data = RaceManager.create_report_data(sorted_data)
        report_format = FormatEnum(args.get("format"))
        return serialize_response(report_format, report_data)


class DriversInformation(Resource):
    def get(self) -> Response:
        """Drivers and their abbreviations for references
        ---
        definitions:
          Information:
              type: object
              properties:
                  data:
                    type: array
                    items:
                        type: object
                        additionalProperties:
                            type: string
                        example:
                            abbreviation: LSW,
                            full_name: Lance Stroll
          NoContent:
              type: object
              properties:
                    massage:
                        type: string
                        example: There is no appropriate database
        parameters:
          - name: order
            in: query
            type: string
            enum: ['asc', 'desc']
            required: false
            default: asc
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            required: false
            default: json
        responses:
          200:
            description: Report of driver's results
            schema:
              $ref: '#/definitions/Information'
          502:
            description: Particular driver statistic
            schema:
              $ref: '#/definitions/NoContent'
        """
        args = request.args
        sorted_data = RaceManager.sort_data(OrderEnum(args.get("order")))
        drivers_info_data = RaceManager.create_drivers_info(sorted_data)
        report_format = FormatEnum(args.get("format"))
        return serialize_response(report_format, drivers_info_data)


class DriversDetails(Resource):
    def get(self, driver_id: str) -> Response:
        """Driver statistic
        ---
        definitions:
          Driver_info:
            type: object
            properties:
              driver_id:
                type: string
                example: VBM
              full_name:
                type: string
                example: Valtteri Bottas
              team:
                type: string
                example: MERCEDES
              lap_time:
                type: string
                example: "01:12.434"
          NoContent:
            type: object
            properties:
                massage:
                    type: string
                    example: There is no appropriate database
          NotFound:
            type: object
            properties:
                massage:
                    type: string
                    example: There is no driver with id=some_driver_id
        parameters:
          - name: driver_id
            in: path
            type: string
            required: true
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            required: false
            default: json
        responses:
          200:
            description: Particular driver statistic
            schema:
              $ref: '#/definitions/Driver_info'
          404:
            description: NOT FOUND
            schema:
              $ref: '#/definitions/NotFound'
          502:
            description: Particular driver statistic
            schema:
              $ref: '#/definitions/NoContent'
        """
        args = request.args
        selected_driver = RaceManager.get_driver(driver_id)
        if not selected_driver:
            abort(HTTPStatus.NOT_FOUND, f"There is no driver with id={driver_id}")
        report_format = FormatEnum(args.get("format"))
        return serialize_response(report_format, selected_driver)
