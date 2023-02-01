import pyperclip
from constants import *
from selenium import webdriver
from pathlib import Path
from os import mkdir

pyperclip.copy(URL_BASE)

# List of courses left (not case sensitive)
# COURSE_LIST = ('ELEC3004', 'STAT2003', 'ELEC2400', 'METR3100',
#                'ELEC3310', 'MECH2100', 'MATH2100',
#                'METR4201', 'CSSE2310', 'MATH3401', 'MATH3101',
#                'MECH3200', 'METR6203', 'METR4202',
#                'ELEC4310', 'MATH3202', 'MATH3201',
#                'METR4912', 'MATH3403', 'MATH3102',
#                'ENGG4900', 'METR4810')
# COURSE_LIST = ('MATH1071', 'ENGG1100', 'ENGG1300', 'ENGG1500',
#                'ENGG1700', 'MATH1061', 'MATH1072', 'CSSE1001',
#                'MATH2001',
#                'MECH2300', 'ELEC2300', 'CSSE2010', 'MATH2400',
#                'MECH2210', 'METR2800', 'ELEC2004', 'STAT1301')
COURSE_LIST = ('MATH1051', 'INFS1200', 'MATH1052', 'MATH2302', 'CSSE2002', 'STAT2201', 'MATH2010', 'COMP3506', 'COMP3702',
               'COMP3710', 'COMP4702', 'COMP2048', 'CSSE3010', 'ECON1010', 'DECO3801', 'STAT3006', 'ELEC3100', 'ECON1020', 
               'ELEC4630', 'CSSE4011', '')


COURSE_LOWER = [code.lower() for code in COURSE_LIST]

def download_course_info(course_code: str, dest_dir: Path, browser: webdriver.Safari): # Only works with Safari
    if (dest_dir / course_code).with_suffix('.html').exists():
        print(f"{course_code.upper()} already in {str(dest_dir)}")
        return
    browser.get(URL_BASE + course_code)
    with open((dest_dir / course_code).with_suffix('.html'), 'w') as file:
        file.write(browser.page_source)

def main():
    course_dir = Path(COURSE_DIR_STR).resolve()
    browser = webdriver.Safari()
    browser.minimize_window()
    if not course_dir.exists():
        mkdir(course_dir)
    for course_code in COURSE_LOWER:
        download_course_info(course_code, course_dir, browser)
    browser.close()

if __name__ == '__main__':
    main()