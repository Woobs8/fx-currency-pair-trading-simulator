from datetime import datetime

def get_local_timezone() -> str:
    local_tz = datetime.utcnow().astimezone().tzinfo
