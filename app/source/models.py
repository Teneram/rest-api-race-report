from peewee import CharField, Model

from app.source.db import db


class Driver(Model):

    abbreviation = CharField(unique=True, primary_key=True, max_length=3)
    full_name = CharField()
    team = CharField()
    lap_time = CharField(null=True)

    class Meta:
        database = db
        table_name = "drivers"


models = [Driver]
