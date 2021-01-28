from ..invalid import InvalidUsage
from datetime import datetime
from ..constant import *


def validateIdYearSem(id: str, year: tuple[int, bool], sem: tuple[int, bool]) -> None:
    if len(id) != 7 or not intTryParse(id)[1]:
        raise InvalidUsage(
            f"Id must be number and has a length of 7",
            status_code=440,
            payload={
                "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "path": f"/course/{id}",
            },
        )
    if not year[1] or not sem[1]:
        raise InvalidUsage(
            f"Year and Semester must be number",
            status_code=441,
            payload={
                "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "path": f"/course/{id}",
            },
        )

    if abs(defaultYear() - year[0]) > 3:
        raise InvalidUsage(
            f"Year difference cannot more than 2 from current academic year ({defaultYear})",
            status_code=442,
            payload={
                "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "path": f"/course/{id}",
                "year": year[0],
            },
        )

    if sem[0] not in [1, 2, 3]:
        raise InvalidUsage(
            f"Semester must be 1, 2, or 3",
            status_code=443,
            payload={
                "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "path": f"/course/{id}",
                "sem": sem[0],
            },
        )
