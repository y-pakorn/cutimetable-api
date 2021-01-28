from datetime import datetime
from ..invalid import InvalidUsage
from typing import Any
from bs4 import BeautifulSoup
import requests
import re
from ..constant import intTryParse


def getCourse(id: str, year: int, sem: int) -> tuple[dict[str, Any], int]:
    firstSessionURL = "https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.QueryCourseScheduleNewServlet"

    secondSessionUrl = f"https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseListNewServlet?examdateCombo=I2019102%2F12%2F1476&studyProgram=S&semester={sem}&acadyearEfd={year}&submit.x=31&submit.y=16&courseno={id}&coursename=&examdate=&examstartshow=&examendshow=&faculty={id[:2]}&coursetype=&genedcode=&cursemester={sem}&curacadyear={year}&examstart=&examend=&activestatus=OFF&acadyear={year}&lang=T&download=download"

    lastSessionUrl = f"https://cas.reg.chula.ac.th/servlet/com.dtm.chula.cs.servlet.QueryCourseScheduleNew.CourseScheduleDtlNewServlet?courseNo={id}&studyProgram=S"

    session = requests.Session()

    session.get(firstSessionURL)
    session.get(secondSessionUrl)
    response = session.get(lastSessionUrl)

    soup = BeautifulSoup(response.content, "html.parser")

    courseJson = {}

    if soup.title:

        table = soup.findAll("table")
        courseInfo = [" ".join(ele.text.split()) for ele in table[1].findAll("tr")[1:]]
        creditHours = [" ".join(ele.text.split()) for ele in table[2].findAll("tr")]
        examDate = [" ".join(ele.text.split()) for ele in table[3].findAll("tr")]
        sections = [
            [" ".join(i.text.split()) for i in ele.findAll("td")[1:]]
            for ele in table[4].findAll("tr")[2:]
        ]

        courseJson["id"] = id
        courseJson["year"] = year
        courseJson["semester"] = sem
        courseJson["name"] = " ".join(courseInfo[2].split()[1:])
        courseJson["fullName"] = courseInfo[-2]
        courseJson["thainame"] = courseInfo[-3]
        courseJson["credits"] = {
            "total": intTryParse(re.findall(r"(\d).\d\sCRE", creditHours[0])[0][0])[0],
            "type": {
                k: intTryParse(v)[0]
                for k, v in re.findall(r"(\w+)\s(\d).\d", creditHours[0])
            },
        }
        courseJson["prerequisite"] = re.findall(r"PRER\s(\d+)", creditHours[-1])
        courseJson["corequisite"] = re.findall(r"COREQ\s(\d+)", creditHours[-1])

        midterm = re.findall(
            r"วันสอบกลางภาค\s:\s(\d+\s[ก-๛\.]+\s\d+)\sเวลา\s([0-9:]+)-([0-9:]+)",
            examDate[0],
        )
        final = re.findall(
            r"วันสอบปลายภาค\s:\s(\d+\s[ก-๛\.]+\s\d+)\sเวลา\s([0-9:]+)-([0-9:]+)",
            examDate[0],
        )

        courseJson["examDate"] = {
            "midterm": {
                "date": None
                if len(midterm) == 0
                else None
                if len(midterm[0]) < 1
                else midterm[0][0],
                "time": None
                if len(midterm) == 0
                else None
                if len(midterm[0]) < 3
                else {
                    "start": midterm[0][1],
                    "end": midterm[0][2],
                },
            },
            "final": {
                "date": None
                if len(final) == 0
                else None
                if len(final[0]) < 1
                else final[0][0],
                "time": None
                if len(final) == 0
                else None
                if len(final[0]) < 3
                else {
                    "start": final[0][1],
                    "end": final[0][2],
                },
            },
        }

        def validateSList(l: str, splitter: str = None) -> bool:
            return l.split(splitter)[0] == "AR" or l.split()[0] == "IA"

        def validateSText(t: str) -> bool:
            return t.strip() == "AR" or t.strip() == "IA"

        def validateSection(section: list, index: int) -> bool:
            if len(section) - 1 < index:
                return True
            return (
                section[index].strip() == "AR"
                or section[index].strip() == "IA"
                or section[index].strip() == ""
            )

        sectionList = [
            {
                "section": re.findall(r"\d{1,2}", section[0])[0],
                "type": None if validateSection(section, 1) else section[1],
                "day": None if validateSection(section, 2) else section[2].split(),
                "time": None
                if validateSection(section, 3)
                else {
                    "start": section[3].split("-")[0],
                    "end": section[3].split("-")[1],
                },
                "bldg": None if validateSection(section, 4) else section[4],
                "room": None if validateSection(section, 5) else section[5],
                "prof": None if validateSection(section, 6) else section[6].split(","),
                "exclamation": None if validateSection(section, 7) else section[7],
                "regis": None
                if validateSection(section, 8)
                else {
                    "current": section[8].split("/")[0],
                    "max": section[8].split("/")[1],
                },
            }
            for section in sections
            if len(section) > 8
        ]

        courseJson["sectionList"] = sectionList

        courseJson["timestamp"] = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")

    statusCode = 200 if len(courseJson) > 0 else 204
    return courseJson, statusCode
