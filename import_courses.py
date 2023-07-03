from pathlib import Path
from course_planner import Plan
from constants import SUMMARY_FILENAME
from csv import reader as csv_reader
from yaml import safe_load
from generate_summary import generate_summary
from course_info_scraper import get_course_info
from pandas import read_excel
import sys

def csv2plan(relative_path: str) -> Plan:
    coursesNotDownloaded = []
    excel_filepath = Path(relative_path).resolve()
    plan = Plan()

    if not excel_filepath.suffix == '.xlsx':
        sys.tracebacklimit = 0
        print(excel_filepath.suffix)
        raise TypeError("Excel file type must be xlsx")

    with open(SUMMARY_FILENAME, 'r') as file:
        config_courses = safe_load(file).keys()

    with open(excel_filepath, 'r', encoding='utf-8-sig') as file:
        dataframes = read_excel(excel_filepath, sheet_name=None)
        
        currentYear = ""
        currentSemType = ""
        
        for line in dataframes:
            if line[0]:
                currentYear = line[0]
            currentSemType = line[1]

            sem = ' '.join((currentYear, currentSemType))

            for course in line[2:]:
                if not course:
                    continue
                if course not in config_courses:
                    coursesNotDownloaded.append(course)
                    continue
                plan.add_courses(sem, course)
        
        print(coursesNotDownloaded)
        # get_course_info(coursesNotDownloaded)
        generate_summary()

    return plan