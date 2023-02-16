from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient
from peewee import SqliteDatabase
from racing_report import RacingDataAnalyzer

from app.app import app
from app.source.models import models
from config import DevelopmentConfig
from constants import DATA_PATH
from db.fill_db import RaceData


@pytest.fixture
def database() -> SqliteDatabase:
    test_db = SqliteDatabase(":memory:")
    test_db.bind(models, bind_refs=False, bind_backrefs=False)
    return test_db


@pytest.fixture
def connect(database: SqliteDatabase) -> Generator:
    database.connect()
    yield
    database.close()


@pytest.fixture
def tables(connect: Generator, database: SqliteDatabase) -> SqliteDatabase:
    database.create_tables(models)
    yield database
    database.drop_tables(models)


@pytest.fixture()
def my_app() -> Generator:
    app.config.from_object(DevelopmentConfig)
    yield app


@pytest.fixture()
def client(my_app: Generator) -> FlaskClient:
    return app.test_client()


@pytest.fixture
@patch.object(RacingDataAnalyzer, "build_report", return_value=RaceData)
def data(data_analyzer_mock: MagicMock) -> RaceData:
    return RaceData(DATA_PATH)


@pytest.fixture()
def app_context() -> Generator:
    with app.app_context():
        yield
