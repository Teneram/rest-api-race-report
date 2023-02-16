from app.source.models import db, models
from db.logger import logging


def create_db_tables() -> None:
    db_tables_logger = logging.getLogger(__name__)
    db_tables_logger.info("Database creation called")
    with db:
        db.create_tables(models)
        db_tables_logger.info("Database created")
