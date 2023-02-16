from constants import DATA_PATH
from db.fill_db import infill_drivers_db

if __name__ == "__main__":
    infill_drivers_db(DATA_PATH)
