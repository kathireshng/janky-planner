from constants import *
import yaml

class Course:
    """Class representing a given UQ course."""

    with open(SUMMARY_FILENAME, 'r') as file:
        COURSE_INFO = yaml.safe_load(file)

    def __init__(self, code: str) -> None:
        """Initialises a new course object with the given course code.

        Parameters:
            code (str): The 4 letter - 4 digit UQ course code.
        """
        self.code = code
        self.prereq = self.COURSE_INFO[code][PREREQ]
        self.incomp = self.COURSE_INFO[code][INCOMP]
    
    def is_prerequisite_to(self, other: 'Course') -> bool:
        for sublist in other.prereq:
            if self in other.prereq:
                return True
        return False

    def is_incompatible_with(self, other: 'Course') -> bool:
        """Checks whether a given course object is incompatible with self.

        Parameters:
            course (Course): The other course to check incompatibility with.

        Returns:
            (bool): True iff self and other courses are incompatible.
        """        
        return other.code in self.incomp

    def __str__(self) -> str:
        """(str): Returns course code as a string."""
        return self.code

    def __eq__(self, other: 'Course') -> bool: # TODO: Check whether equality works without this method (because __repr__ might be enough)
        """Compares self and other courses' codes, true iff codes are equal.

        Parameters:
            course (Course): The other course to compare self with.
        
        Returns:
            (bool): True iff both courses' codes are the same.
        """
        return self.code == other.code
    
    def __repr__(self) -> str:
        return self.code

    def __hash__(self) -> int:
        return hash(self.code)


class Semester:
    def __init__(self, num: int, *courses: Course) -> None:
        self.num = num
        self.name = SEM_NAMES[num]
        self.courses = list(courses)
        self._purge_repeated_courses()
        if self.is_summer_sem() and len(courses) > SUM_SEM_MAX:
            print("This is a summer semester course which has at most two"
                    "courses.\n More than two have been given.\n"
                    "This semester will be created without any courses.")
            self.courses = []
        
    def _purge_repeated_courses(self):
        for courseA in self.courses:
            for courseB in self.courses:
                if courseA == courseB:
                    self.courses.remove(courseB)
                    self._purge_repeated_courses() 

    def get_course_names(self) -> list[str]:
        name_list = []
        for course in self.courses:
            name_list.append(course)
        return name_list

    def is_summer_sem(self) -> bool:
        return self.num % 3 == 2
    
    def is_full(self) -> bool:
        if self.is_summer_sem():
            return len(self.courses) <= SUM_SEM_MAX
        return len(self.courses) <= REG_SEM_MAX

    def max_course_capacity(self) -> int:
        return SUM_SEM_MAX if self.is_summer_sem() else REG_SEM_MAX

    def _get_possible_incompatiblities(self) -> list[str]:
        incomp_list = []
        for course in self.courses:
            incomp_list.append(course.incomp)
        return incomp_list

    def get_incompatibilities(self) -> list[str]:
        incomp_list = []
        for course in self._get_possible_incompatiblities():
            if course in self.courses:
                incomp_list.append(course)
        return incomp_list
    
    def any_incompatibilites(self) -> bool:
        return bool(self.get_incompatibilities())
    
    def add_courses(self, *courses: Course) -> None:
        if len(self.courses) + len(courses) > self.max_course_capacity():
            print(
                f"{self.name} can contain at most "
                f"{self.max_course_capacity()} courses.\n"
                f"At most, {REG_SEM_MAX - len(courses)} " 
                "more courses can be added to this semester."
            )
            return
        self.courses.append(*courses)

    def remove_course(self, course: Course) -> None:
        if course not in self.courses:
            print(f"{course} not in {self.name}")
            return
        self.courses.remove(course)

    def is_before(self, other: 'Semester') -> bool:
        return self.num < other.num
    
    def is_after(self, other: 'Semester') -> bool:
        return self.num > other.num


class Plan:
    def __init__(self) -> None:
        self.semesters = self._init_semesters()
    
    def _init_semesters(self) -> list[Semester]:
        sem_list = []
        for sem_num in range(len(SEM_NAMES)):
            sem_list.append(Semester(sem_num))
        return sem_list

    def add_courses(self, courses: list[Course], sem: Semester) -> None:
        sem.add_courses(courses)

    def remove_course(self, course: Course) -> None:
        for sem in self.semesters:
            for existing_course in sem.courses:
                if course == existing_course:
                    sem.remove_course(course)

    def swap_courses(course_1: Course, course_2: Course) -> None:
        pass

    def are_prerequisities_met(self) -> bool:
        pass

    def are_incompatibilites_met(self) -> bool:
        for semester in self.semesters:
            if semester.get_incompatibilities():
                return True
        return False