from os import path
from datetime import datetime
from time import timezone
import pytz

def get_modification_time(fp: str) -> datetime:
    modifification_ts = path.getmtime(fp)
    return datetime.utcfromtimestamp(modifification_ts)
