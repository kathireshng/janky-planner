import re
from pathlib import Path
import yaml
from constants import *
from bs4 import BeautifulSoup

course_dict = {}
courses_downloads_dir = Path('Courses') #FIXME Currently hardcoded. Directory should be specified from constants.py

def filename2code(filename: str) -> str:
    return filename.split('.')[0].upper()

def update_names():
    for course_file in courses_downloads_dir.iterdir():
        if '.html' not in course_file.name:
            continue
        course_dict[filename2code(course_file.name)] = {
            SEM_OFFERED: None,
            PREREQ: None,
            INCOMP: None
        }

def pull_course_codes(line: str) -> list:
    return re.findall('[A-Z]{4}\d{4}', line)

def get_prerequisites(line: str) -> list[list[str]]: # FIXME: Sometimes just gets it wrong, e.g. returns [['MATH1051'], ['MATH1071']] instead of [['MATH1051', 'MATH1071']]
    prereq_list = [pull_course_codes(group) for group in re.findall('\((.*?)\)', line)]
    nested_course_list = [course for group in prereq_list for course in group]
    all_course_list = pull_course_codes(line)
    for remaining_course in list(set(all_course_list) - set(nested_course_list)):
        prereq_list.append([remaining_course])
    return prereq_list

def pull_sem_offered(html: str) -> list[str]:
    current_offerings_table = BeautifulSoup(html, 'html.parser').find('table', id="course-current-offerings")
    sems_offered_list_soup = current_offerings_table.find_all('a', id=re.compile('course-offering-.-sem'))
    sems_offered_list_str = list(set([sem for soup_obj in sems_offered_list_soup for sem in (SEM_1, SEM_2, SUM_SEM) if sem in soup_obj.text]))

    return sems_offered_list_str

#TODO: Refactor update_details() and pull_course_codes() to fit within 80 char line length.
#TODO: Refactor get prereqs and create dedicated incomps fetcher using BeautifulSoup
def update_details():
    for course_file in courses_downloads_dir.iterdir():
        if '.html' not in course_file.name:
            continue
        with open(str(course_file), 'r') as file:
            html = file.read()
            file.seek(0)
            for line in file:
                if 'course-prerequisite' in line:
                    course_dict[filename2code(course_file.name)][PREREQ] = get_prerequisites(line)
                elif 'course-incompatible' in line:
                    course_dict[filename2code(course_file.name)][INCOMP] = pull_course_codes(line)
        if not html:
            print('NO HTML!!!!')
            print(course_file.name)
        else:
            print(course_file.name, "ALL GOOD!", sep=': ')
        course_dict[filename2code(course_file.name)][SEM_OFFERED] = pull_sem_offered(html)
    

def add_default_course():
    course_dict[DEFAULT] = {}
    course_dict[DEFAULT][PREREQ] = None
    course_dict[DEFAULT][INCOMP] = None
    course_dict[DEFAULT][SEM_OFFERED] = [SEM_1, SEM_2]

def write2yaml():
    with open(SUMMARY_FILENAME, 'w') as file:
        file.write(yaml.dump(course_dict))

def main():
    update_names()
    update_details()
    add_default_course()
    write2yaml()

if __name__ == '__main__':
    main()