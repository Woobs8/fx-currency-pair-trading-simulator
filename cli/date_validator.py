from datetime import datetime, timezone
import argparse
from utils.timezone import get_local_timezone


def valid_date(date: str) -> datetime:
    for fmt in ('%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(date, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    msg = "Not a valid date: '{0}'.".format(date)
    raise argparse.ArgumentTypeError(msg)