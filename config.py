import os


class DevelopmentConfig:
    DEBUG = True
    TESTING = True
    DB_PATH = os.environ.get("DB_PATH")
