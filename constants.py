
DEBUG = True

# Filename of summary yaml file (DO NOT FORGET .yaml EXT)
SUMMARY_FILENAME = 'summary.yaml'

# URL info
URL_BASE = 'https://my.uq.edu.au/programs-courses/course.html?course_code='

# Relative location of Courses folder with html files
COURSE_DIR_STR = 'Courses'

# Default course name
DEFAULT = 'DEFAULT'

# Dictionary key values
SEM_OFFERED = 'sem offered'
PREREQ = 'prerequisites'
INCOMP = 'incompatible'
UNITS = 'units'

#TODO figure out a more succinct way to represent each semester's name
# Semester names
HIGHSCHOOL_COURSES = 'High School Courses'
YR1_SEM1 = 'Year 1 Semester 1'
YR1_SEM2 = 'Year 1 Semester 2'
YR1_SUMMER = 'Year 1 Summer Semester'
YR2_SEM1 = 'Year 2 Semester 1'
YR2_SEM2 = 'Year 2 Semester 2'
YR2_SUMMER = 'Year 2 Summer Semester'
YR3_SEM1 = 'Year 3 Semester 1'
YR3_SEM2 = 'Year 3 Semester 2'
YR3_SUMMER = 'Year 3 Summer Semester'
YR4_SEM1 = 'Year 4 Semester 1'
YR4_SEM2 = 'Year 4 Semester 2'
YR4_SUMMER = 'Year 4 Summer Semester'
YR5_SEM1 = 'Year 5 Semester 1'
YR5_SEM2 = 'Year 5 Semester 2'
YR5_SUMMER = 'Year 5 Summer Semester'
YR6_SEM1 = 'Year 6 Semester 1'
YR6_SEM2 = 'Year 6 Semester 2'
YR6_SUMMER = 'Year 6 Summer Semester'

SEM_NAMES = (
    YR1_SEM1, YR1_SEM2, YR1_SUMMER,
    YR2_SEM1, YR2_SEM2, YR2_SUMMER,
    YR3_SEM1, YR3_SEM2, YR3_SUMMER,
    YR4_SEM1, YR4_SEM2, YR4_SUMMER,
    YR5_SEM1, YR5_SEM2, YR5_SUMMER,
    YR6_SEM1, YR6_SEM2, YR6_SUMMER
)

SEM_NAMES_ARRAY = ('',
    ('', YR1_SEM1, YR1_SEM2, YR1_SUMMER),
    ('', YR2_SEM1, YR2_SEM2, YR2_SUMMER),
    ('', YR3_SEM1, YR3_SEM2, YR3_SUMMER),
    ('', YR4_SEM1, YR4_SEM2, YR4_SUMMER),
    ('', YR5_SEM1, YR5_SEM2, YR5_SUMMER),
    ('', YR6_SEM1, YR6_SEM2, YR6_SUMMER)
)

SEM_1 = 'Semester 1'
SEM_2 = 'Semester 2'
SUM_SEM = 'Summer Semester'

# Maximum courses for each sem
SUM_SEM_MAX = 2
REG_SEM_MAX = 5


# High school courses
PHYS = 'Physics'
CHEM = 'Chemistry'
SPEC = 'Specialist Mathematics'
METHODS = 'Mathematical Methods'

HS_COURSES = (PHYS, CHEM, SPEC, METHODS)