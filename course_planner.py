from constants import *
import yaml

class Course:
    """Class representing a given UQ course."""

    with open(SUMMARY_FILENAME, 'r') as file:
        courseInfo = yaml.safe_load(file)

    def __init__(self, code: str) -> None:
        """Initialises a new course object with the given course code.

        Parameters:
            code (str): The 4 letter - 4 digit UQ course code.
        """
        self.code = code
        self.prereq = self.courseInfo[code][PREREQ]
        self.incomp = self.courseInfo[code][INCOMP]
    
    def get_code(self) -> str:
        """(str): Returns the course's code."""
        return self.code

    def get_prerequisites(self) -> list[list[str]]:
        """(list[list[str]]): Returns a nested list of the course's 
        prerequisites' codes. 

        Example: 
            Course('ELEC2400').get_prerequisites() returns 
            [['MATH1051', 'MATH1071'], ['MATH1052', 'MATH1072'], ['ENGG1300']]

            which represents: (MATH1051 or MATH1071) and (MATH1052 or MATH1072)
            and ENGG1300.
        """
        return self.prereq

    def get_incompatible(self) -> list[str]:
        """(list[str]): Returns a list of incompatible courses' codes"""
        return self.incomp

    def is_incompatible_with(self, course: 'Course') -> bool:
        """Checks whether a given course object is incompatible with self.

        Parameters:
            course (Course): The other course to check incompatibility with.

        Returns:
            (bool): True iff self and other courses are incompatible.
        """        
        return course.get_code() in self.incomp

    def __str__(self) -> str:
        """(str): Returns course code as a string."""
        return self.get_code()

    def __eq__(self, other: 'Course') -> bool:
        """Compares self and other courses' codes, true iff codes are equal.

        Parameters:
            course (Course): The other course to compare self with.
        
        Returns:
            (bool): True iff both courses' codes are the same.
        """
        return self.get_code() == other.get_code()


class Semester:
    def __init__(self, name, courses: list[Course]=[]) -> None:
        self.name = name
        self.courses = courses
        self._purge_repeated_courses()
        if self.is_summer_sem() and len(courses) > SUM_SEM_MAX:
            print("This is a summer semester course which has at most two"
                    "courses.\n More than two have been given.\n"
                    "This semester will be created without any courses.")
            self.courses = []
        
    def _purge_repeated_courses(self):
        for courseA in self.get_courses():
            for courseB in self.get_courses():
                if courseA == courseB:
                    self.courses.remove(courseB)
                    self._purge_repeated_courses() #TODO Write global function that purges repeated courses or semesters for both
                                                   # Course and Semester classes.
    def get_name(self):
        return SEM_NAME_TUPLE[self.name]

    def get_courses(self) -> list[Course]:
        return self.courses

    def get_course_names(self) -> list[str]:
        name_list = []
        for course in self.get_courses():
            name_list.append(course.get_code())
        return name_list

    def is_summer_sem(self) -> bool:
        return self.name % 3 == 0
    
    def is_full(self) -> bool:
        if self.is_summer_sem():
            return len(self.get_courses()) <= SUM_SEM_MAX
        return len(self.get_courses()) <= REG_SEM_MAX

    def get_max_courses(self) -> int:
        return SUM_SEM_MAX if self.is_summer_sem() else REG_SEM_MAX

    def _get_possible_incompatiblities(self) -> list[str]:
        incomp_list = []
        for course in self.get_courses():
            incomp_list.append(course.get_incompatible())
        return incomp_list

    def get_incompatibilities(self) -> list[str]:
        incomp_list = []
        for course_name in self._get_possible_incompatiblities():
            if course_name in self.get_course_names():
                incomp_list.append(course_name)
        return incomp_list
    
    def any_incompatibilites(self) -> bool:
        return bool(self.get_incompatibilities())
    
    def add_courses(self, courses: list[Course]) -> None:
        if len(self.get_courses()) + len(courses) > self.get_max_courses():
            print(
                f"{self.get_name()} can contain at most "
                f"{self.get_max_courses()} courses.\n"
                f"At most, {REG_SEM_MAX - len(courses)} " 
                "more courses can be added to this semester."
            )
            return
        self.courses.extend(courses)

    def remove_course(self, course: Course) -> None:
        pass


class Plan:
    def __init__(self, semesters: list[Semester]) -> None:
        self.semesters = semesters
        self._purge_repeated_sems()

    def _purge_repeated_sems(self): 
        for semA in self.get_semesters():
            for semB in self.get_semesters():
                if semA.get_name() == semB.get_name():
                    self.semesters.remove(semB)
                    self._purge_repeated_sems() #TODO Implement error message to inform user of semester duplication.

    def get_semesters(self) -> list[Semester]:
        return self.semesters

    def get_required_courses(self) -> list[str]:
        pass

    def add_courses(self, courses: list[Course], sem: Semester) -> None:
        sem.add_courses(courses)

    def remove_course(self, course: Course) -> None:
        pass

    def swap_courses(course_1: str, course_2: str) -> None:
        pass

    def are_prerequisities_met(self) -> bool:
        pass

    def are_incompatibilites_met(self) -> bool:
        for semester in self.get_semesters():
            if semester.get_incompatibilities():
                return True
        return False