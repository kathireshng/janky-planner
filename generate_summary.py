import re
from pathlib import Path
import yaml
from constants import *

course_dict = {}
courses_downloads_dir = Path('Courses') #FIXME Currently hardcoded. Directory should be specified from constants.py

def filename2code(filename: str) -> str:
    return filename.split('.')[0].upper()

def update_names():
    for course_file in courses_downloads_dir.iterdir():
        if '.html' not in course_file.name:
            continue
        course_dict[filename2code(course_file.name)] = {
            SEM_OFFERED: [SEM_1, SEM_2],
            PREREQ: None,
            INCOMP: None
        }

def pull_course_codes(line: str) -> list:
    return re.findall('[A-Z]{4}\d{4}', line)

def get_prerequisites(line: str) -> list[list[str]]:
    prereq_list = [pull_course_codes(group) for group in re.findall('\((.*?)\)', line)]
    nested_course_list = [course for group in prereq_list for course in group]
    all_course_list = pull_course_codes(line)
    for remaining_course in list(set(all_course_list) - set(nested_course_list)):
        prereq_list.append([remaining_course])
    return prereq_list

#TODO: Refactor update_details() and pull_course_codes() to fit within 80 char line length.
def update_details():
    for course_file in courses_downloads_dir.iterdir():
        if '.html' not in course_file.name:
            continue
        with open(str(course_file), 'r') as file:
            for line in file:
                if 'course-prerequisite' in line:
                    course_dict[filename2code(course_file.name)][PREREQ] = get_prerequisites(line)
                elif 'course-incompatible' in line:
                    course_dict[filename2code(course_file.name)][INCOMP] = pull_course_codes(line)

def write2yaml():
    with open(SUMMARY_FILENAME, 'w') as file:
        file.write(yaml.dump(course_dict))

def main():
    update_names()
    update_details()
    write2yaml()

if __name__ == '__main__':
    main()