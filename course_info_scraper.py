from pyautogui import *
from time import sleep
import pyperclip
from constants import *
#TODO Specify download location from constants.py, rather than manually selecting before download

pyperclip.copy(URL_BASE)

# List of courses left (not case sensitive)
# COURSE_LIST = ('ELEC3004', 'STAT2003', 'ELEC2400', 'METR3100',
#                'ELEC3310', 'MECH2100', 'MATH2100',
#                'METR4201', 'CSSE2310', 'MATH3401', 'MATH3101',
#                'MECH3200', 'METR6203', 'METR4202',
#                'ELEC4310', 'MATH3202', 'MATH3201',
#                'METR4912', 'MATH3403', 'MATH3102',
#                'ENGG4900', 'METR4810')
COURSE_LIST = ('MATH1071', 'ENGG1100', 'ENGG1300', 'ENGG1500',
               'ENGG1700', 'MATH1061', 'MATH1072', 'CSSE1001',
               'MATH2001',
               'MECH2300', 'ELEC2300', 'CSSE2010', 'MATH2400',
               'MECH2210', 'METR2800', 'ELEC2004', 'STAT1301')
COURSE_LOWER = [code.lower() for code in COURSE_LIST]

PAUSE = 1

def spotlight_search():
    keyDown('command')
    press('space')
    keyUp('command')

def open_safari():
    spotlight_search()
    typewrite('safari')
    hotkey('enter')
    sleep(0.5)

def search_site(course_code: str):
    hotkey('command', 'l')
    hotkey('command', 'v')
    typewrite(course_code)
    hotkey('enter')
    sleep(5)

def download_page(course_code: str) -> None:
    """
    Downloads the page to the specified directory.
    """
    hotkey('command', 's')
    sleep(1)
    typewrite(course_code)
    sleep(0.1)
    hotkey('enter')
    sleep(0.5)

def main():
    open_safari()
    for course_code in COURSE_LOWER:
        search_site(course_code)
        download_page(course_code)

if __name__ == '__main__':
    main()