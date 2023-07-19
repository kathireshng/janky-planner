import re
from pathlib import Path
import yaml
from constants import *
from bs4 import BeautifulSoup


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

def pull_course_codes(line: str) -> list:
    codes = re.findall('[A-Z]{4}\d{4}', line)
    for highschool_course in HS_COURSES:
        if highschool_course in line:
            codes.append(highschool_course)
    return codes

def pull_incompatibles(html: str) -> list[str]:
    incompsLine = BeautifulSoup(html, 'html.parser').find('p', id='course-incompatible')
    if not incompsLine:
        return
    return pull_course_codes(incompsLine.text)

def pull_prerequisites(html: str) -> list[list[str]]:
    prereqsLine = BeautifulSoup(html, 'html.parser').find('p', id='course-prerequisite')
    if not prereqsLine:
        return
    prereqsText = prereqsLine.text

    if not '(' in prereqsText or not [pull_course_codes(textInBrackets) for textInBrackets in re.findall('\((.*?)\)', prereqsText) if pull_course_codes(textInBrackets)]: # Assumption: Prerequisites without brackets have only one of "and" or "or" between courses
        if ' and ' in prereqsText:
            final_list = [[courseCode] for courseCode in pull_course_codes(prereqsText)]
        
        elif ' or ' in prereqsText or ',' in prereqsText:
            final_list = [pull_course_codes(prereqsText)]
       
        else:
            final_list = [pull_course_codes(prereqsText)]
    
    else:
        prereqList = [pull_course_codes(group) for group in re.findall('\((.*?)\)', prereqsText) if pull_course_codes(group)]
        nested_course_list = [course for group in prereqList for course in group]
        all_course_list = pull_course_codes(prereqsText)
        for remaining_course in list(set(all_course_list) - set(nested_course_list)):
            prereqList.append([remaining_course])
        final_list = prereqList

    return final_list

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