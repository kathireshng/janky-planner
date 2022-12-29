from constants import *
import yaml

class Course:
    with open(SUMMARY_FILENAME, 'r') as file:
        courseInfo = yaml.load(file)

    def __init__(self, code) -> None:
        self.code = code
        self.prereq = self.courseInfo[code][PREREQ]
        self.incomp = self.courseInfo[code][INCOMP]
    
    def is_incompatible_with(self, course: 'Course') -> bool:
        return course.get_code() in self.incomp

    def get_code(self) -> str:
        return self.code

    def get_prerequisites(self):
        return self.prereq

    def get_incompatible(self) -> list[str]:
        return self.incomp

    def __str__(self) -> str:
        pass


class Semester:
    def __init__(self, name, course1, course2, course3=None, course4=None) -> None:
        self.name = name
        self.courses = list(course1, course2)
        if course3:
            self.courses.append(course3) 
        if course4:
            self.courses.append(course4)

        if self.is_summer_sem() and course3:
            print(ERR_MSG_TOO_MANY_COURSES)
            self.courses = list(course1, course2)

    def is_summer_sem(self) -> bool:
        return self.name % 3 == 0


class Plan:
    def __init__(self) -> None:
        pass

    def get_required_courses(self) -> list[str]:
        pass

    def add_course(self) -> None:
        pass

    def remove_course(self) -> None:
        pass

    def swap_courses(course_1: str, course_2: str) -> None:
        pass

    def are_prerequisities_met(self) -> bool:
        pass
