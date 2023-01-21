from constants import *
import yaml

with open(SUMMARY_FILENAME, 'r') as file:
        COURSE_INFO = yaml.safe_load(file)

class Semester:
    def __init__(self, num: int, *courses: str) -> None:
        self.num = num
        self.name = SEM_NAMES[num]
        self.courses = list(courses)
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

    def is_summer_sem(self) -> bool:
        return self.num % 3 == 2

    def get_type(self) -> str:
        if self.is_summer_sem():
            return SUM_SEM
        if self.num % 3 == 1:
            return SEM_2
        return SEM_1
    
    def is_full(self) -> bool:
        if self.is_summer_sem():
            return (len(self.courses) == SUM_SEM_MAX)
        return (len(self.courses) == REG_SEM_MAX)

    def max_course_capacity(self) -> int:
        return SUM_SEM_MAX if self.is_summer_sem() else REG_SEM_MAX

    def _get_possible_incompatiblities(self) -> list[str]:
        incomp_list = []
        for course in self.courses:
            incomp_list.extend(COURSE_INFO[course][INCOMP])
        return incomp_list

    def get_incompatibilities(self) -> list[str]:
        incomp_list = []
        for course in self._get_possible_incompatiblities():
            if course in self.courses:
                incomp_list.append(course)
        return incomp_list
    
    def any_incompatibilites(self) -> bool:
        return bool(self.get_incompatibilities())
    
    def add_courses(self, *courses: str) -> None:
        if len(self.courses) + len(courses) > self.max_course_capacity():
            print(
                f"{self.name} can contain at most "
                f"{self.max_course_capacity()} courses.\n"
                f"At most, {REG_SEM_MAX - len(courses)} " 
                "more courses can be added to this semester."
            )
            return
        for course in courses:
            if self.get_type() not in COURSE_INFO[course][SEM_OFFERED]:
                print(f"{course} is not offered in {self.get_type()}",
                       "Aborting add_courses().", sep='\n')
                return

        self.courses.extend(courses)

    def remove_course(self, course: str) -> None:
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

    def _get_course_list(self) -> list[str]:
        course_list = []
        for sem in self.semesters:
            for course in sem:
                if not course:
                    continue
                course_list.append(course)
        return course_list

    def _get_semester_of_course(self, course: 'str') -> Semester:
        for sem in self.semesters:
            if course in sem:
                return sem

    def _plan_has_course(self, course: str) -> bool:
        for sem in self.semesters:
            if course in sem.courses:
                return True
        return False

    def add_courses(self, sem: Semester, *courses: str) -> None:
        sem.add_courses(*courses)

    def remove_course(self, course: str) -> None:
        for sem in self.semesters:
            for existing_course in sem.courses:
                if course == existing_course:
                    sem.remove_course(course)

    def swap_courses(self, course_1: str, course_2: str) -> None:
        sem_1 = self._get_semester_of_course(course_1)
        sem_2 = self._get_semester_of_course(course_2)

        if not (sem_1 and sem_2):
            if not sem_1:
                print(f"{course_1} not in plan.")
            if not sem_2:
                print(f"{course_1} not in plan.")
            return

        if sem_1.name == sem_2.name:
            print(f"{course_1} and {course_2} are both already in {sem_1.name}")
            return

        if not(COURSE_INFO[course_1][SEM_OFFERED] == sem_2.get_type() 
           and COURSE_INFO[course_2][SEM_OFFERED] == sem_1.get_type()):
            if COURSE_INFO[course_1][SEM_OFFERED] != sem_2.get_type():
                print(f"{course_1} not offered in {sem_2.get_type()} ")
            if COURSE_INFO[course_1][SEM_OFFERED] != sem_2.get_type():
                print(f"{course_2} not offered in {sem_1.get_type()} ")
            return

        sem_1.remove_course(course_1)
        sem_2.remove_course(course_2)
        sem_1.add_courses(course_2)
        sem_2.add_courses(course_1)

    def are_prerequisities_met(self) -> bool:
        course_list = self._get_course_list()
        for course in course_list:
            for prereq_list in COURSE_INFO[course][PREREQ]:
                for prereq_course in prereq_list:
                    if self._plan_has_course(prereq_course):
                        continue
                    return False
        return True

    def any_incompatiblities(self) -> bool:
        for sem in self.semesters:
            if sem.get_incompatibilities():
                return True
        return False
    
def main():
    pass

if __name__=='__main__':
    main()