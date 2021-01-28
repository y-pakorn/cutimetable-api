from typing import Any
from datetime import date


def defaultYear() -> int:
    year = date.today().year
    month = date.today().month
    if month > 5:
        return year + 543
    else:
        return year + 542


def defaultSem() -> int:
    month = date.today().month
    if month > 1 and month < 5:
        return 3
    elif month > 10 or month == 1:
        return 2
    else:
        return 1


def intTryParse(value: Any) -> tuple[Any, bool]:
    try:
        return int(value), True
    except ValueError:
        return value, False
