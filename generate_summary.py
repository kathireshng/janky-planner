import re
from pathlib import Path
import yaml
from constants import *
from bs4 import BeautifulSoup
from bs4 import element

def filename2code(filename: str) -> str:
    return filename.split('.')[0].upper()

def update_names(course_dict: dict, course_html_dir: Path):
    for course_file in course_html_dir.iterdir():
        if '.html' not in course_file.name:
            continue
        course_dict[filename2code(course_file.name)] = {
            SEM_OFFERED: None,
            PREREQ: None,
            INCOMP: None
        }

# make a function that finds four letters followed by four numbers. for example, mech2300, elec2004. Letters can be any case

# def pull_course_codes(tag) -> list[str]:
#     codeList = []
#     codes = re.findall(''[A-Z]{4}\d{4}'', tag.text)

def pull_course_codes(tag) -> list[str]:
    codeList = []
    
    codes = re.findall('[A-Z]{4}\d{4}', tag.text)
    if tag.text.strip() and not bool(codes):
        return 'Special rules apply'
    
    if not codes:
        codes = re.findall('[A-Z]{4}\d{4}', tag.find_next('p').text)
    codeList.extend(codes)
        
    # for highschool_course in HS_COURSES:
    #     if highschool_course in line:
    #         codes.append(highschool_course)
    return codeList
    
def pull_incompatibles(html: str) -> list[str]:
    parser = BeautifulSoup(html, 'html.parser')
    incompsResultSet = parser.find_all(id='course-incompatible')
    if not incompsResultSet:
        return
    incompsTag = incompsResultSet[0]
    return pull_course_codes(incompsTag)

def pull_prerequisites(html: str) -> list[str]:
    parser = BeautifulSoup(html, 'html.parser')
    prereqsResultSet = parser.find_all(id='course-prerequisite')
    if not prereqsResultSet:
        return
    prereqsTag = prereqsResultSet[0]
    return pull_course_codes(prereqsTag)

def pull_sem_offered(html: str) -> list[str]:
    current_offerings_table = BeautifulSoup(html, 'html.parser').find('table', id="course-current-offerings")
    if not current_offerings_table:
        return
    sems_offered_list_soup = current_offerings_table.find_all('a', id=re.compile('course-offering-.-sem'))
    sems_offered_list_str = list(set([sem for soup_obj in sems_offered_list_soup for sem in (SEM_1, SEM_2, SUM_SEM) if sem in soup_obj.text]))

    return sems_offered_list_str

def pull_units(html: str) -> int:
    unitsLine = BeautifulSoup(html, 'html.parser').find('p', id='course-units')
    if not unitsLine:
        return
    return int(unitsLine.text.split(' ')[0])

def update_details(course_dict: dict, courses_html_dir: Path):
    for course_file in courses_html_dir.iterdir():
        course_filename = course_file.name
        if '.html' not in course_filename:
            continue
        with open(str(course_file), 'r') as file:
            html = file.read()
        course_dict[filename2code(course_filename)][PREREQ] = pull_prerequisites(html)
        course_dict[filename2code(course_filename)][INCOMP] = pull_incompatibles(html)
        course_dict[filename2code(course_filename)][SEM_OFFERED] = pull_sem_offered(html)
        course_dict[filename2code(course_filename)][UNITS] = pull_units(html)

    
def add_default_course(course_dict: dict):
    course_dict[DEFAULT] = {}
    course_dict[DEFAULT][PREREQ] = None
    course_dict[DEFAULT][INCOMP] = None
    course_dict[DEFAULT][SEM_OFFERED] = [SEM_1, SEM_2]

def write2yaml(course_dict: dict, summary_filename=SUMMARY_FILENAME, overwrite_existing=False):
    if not overwrite_existing and Path(summary_filename).exists():
        with open(summary_filename, 'r') as file:
            existingCourseDict = yaml.safe_load(file)
            course_dict.update(existingCourseDict)
    with open(summary_filename, 'w') as file:
        file.write(yaml.dump(course_dict))

def generate_summary():
    course_dict = {}
    courses_html_path = Path(COURSE_DIR_STR)

    update_names(course_dict, courses_html_path)
    update_details(course_dict, courses_html_path)
    add_default_course(course_dict)
    write2yaml(course_dict)

if __name__ == '__main__':
    generate_summary()