import pyperclip
from constants import *
from selenium import webdriver
from pathlib import Path
from os import mkdir

BENGG_COURSE_LIST = 'https://my.uq.edu.au/programs-courses/requirements/program/2455/2021'

def scrape_course_names(url: str) -> list[str]:
    browser = webdriver.Safari()
    browser.minimize_window()
    browser.get(url)
    course_list = browser.find_elements_by_class_name('coursebox')
    course_names = [course.text for course in course_list]
    browser.close()
    return course_names

def download_course_info(course_code: str, dest_dir: Path, browser: webdriver.Safari): # Only works with Safari
    if (dest_dir / course_code).with_suffix('.html').exists():
        print(f"{course_code.upper()} already in {str(dest_dir)}")
        return
    browser.get(URL_BASE + course_code)
    with open((dest_dir / course_code).with_suffix('.html'), 'w') as file:
        file.write(browser.page_source)

def get_course_info(course_list: list[str], dest_dir=COURSE_DIR_STR):
    course_dir = Path(dest_dir).resolve()
    browser = webdriver.Safari()
    browser.minimize_window()
    if not course_dir.exists():
        mkdir(course_dir)
    for course_code in course_list:
        download_course_info(course_code, course_dir, browser)
    browser.close()

def get_course_codes_from_webpage(url: str):
    browser = webdriver.Safari()
    browser.minimize_window()
    browser.get(url)
    text = browser.page_source
    browser.close()
    course_codes = []
    for i in range(len(text)):
        candidate_code = text[i:i+8]
        if candidate_code in course_codes:
            continue
        if candidate_code[0:4].isalpha() and candidate_code[4:8].isnumeric():
            course_codes.append(text[i:i+8].upper())
    course_codes.sort()
    for course_code in course_codes:
        print(course_code)

def main():
    get_course_codes_from_webpage(BENGG_COURSE_LIST)

if __name__ == '__main__':
    main()