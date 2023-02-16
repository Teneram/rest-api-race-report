import os
from enum import Enum

DATA_PATH = os.environ.get("DATA_PATH")
VERSION = 1
ROOT_NAME = "report"


class FormatEnum(Enum):
    json = "json"
    xml = "xml"
    none = None


class OrderEnum(Enum):
    asc = "asc"
    desc = "desc"
    none = None
