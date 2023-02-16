from peewee import SqliteDatabase

from config import DevelopmentConfig

db = SqliteDatabase(DevelopmentConfig.DB_PATH)
