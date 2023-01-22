from constants import *
import yaml
from pprint import pprint
from my_courses import initialise_my_plan # See Line 211-2 for why this is here
import webbrowser

with open(SUMMARY_FILENAME, 'r') as file:
        COURSE_INFO = yaml.safe_load(file)

#TODO MAKE ATTRIBUTES PRIVATE AND HAVE GETTERS AND SETTERS FOR THEM

class Semester:
    def __init__(self, name: str, *courses: str) -> None:
        if not name in SEM_NAMES:
            raise NameError(f"{name} is not a valid semester name!")
        self.name = name
        self._num = self._get_sem_num()
        self.courses = list(courses)
        if self.get_type() == SUM_SEM and len(courses) > SUM_SEM_MAX:
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

    def _get_sem_num(self):
        nums = [int(word) for word in self.name.split() if word.isdigit()]
        if len(nums) == 1:
            return 3*(nums[0])
        year, sem = nums
        return 3*(year - 1) + sem

    def get_type(self) -> str:
        if self._num % 3 == 0:
            return SUM_SEM
        if self._num % 3 == 1:
            return SEM_1
        return SEM_2
    
    def is_full(self) -> bool:
        if self.get_type() == SUM_SEM:
            return (len(self.courses) == SUM_SEM_MAX)
        return (len(self.courses) == REG_SEM_MAX)

    def max_course_capacity(self) -> int:
        return SUM_SEM_MAX if self.get_type() == SUM_SEM else REG_SEM_MAX

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
        return self._num < other._num
    
    def is_after(self, other: 'Semester') -> bool:
        return self._num > other._num


class Plan:
    def __init__(self) -> None:
        self.semesters = self._init_semesters()
    
    def _init_semesters(self) -> list[Semester]:
        sem_list = []
        for sem_name in SEM_NAMES:
            sem_list.append(Semester(sem_name))
        return sem_list

    def _get_course_list(self) -> list[str]:
        course_list = []
        for sem in self.semesters:
            for course in sem.courses:
                if not course:
                    continue
                course_list.append(course)
        return course_list

    def _get_semester_of_course(self, course: 'str') -> Semester:
        for sem in self.semesters:
            if course in sem.courses:
                return sem

    def _has_course(self, course: str) -> bool:
        for sem in self.semesters:
            if course in sem.courses:
                return True
        return False

    def _get_sem_with_name(self, sem_name: str) -> Semester:
        for sem in self.semesters:
            if not sem.name == sem_name:
                continue
            return sem

    def add_courses(self, sem_name: str, *courses: str) -> None:
        if not sem_name in SEM_NAMES:
            print(f"{sem_name} is not a valid semester name.\n"
                   "Use one of: ")
            for name in SEM_NAMES:
                print('\t', name)
            print("\nOr a variable name such as YR1_SEM2 or YR3_SUMMER.")
            return
        
        for course in courses:
            if not course in self._get_course_list():
                continue
            print(f"{course} already in plan, in {self._get_semester_of_course(course).name}")
            return
        self._get_sem_with_name(sem_name).add_courses(*courses)

    def remove_course(self, course: str) -> None:
        if not self._has_course(course):
            print(f"Plan already does not have {course}")
            return
        self._get_semester_of_course(course).remove_course(course)

    def swap_courses(self, course_A: str, course_B: str) -> None:
        sem_A = self._get_semester_of_course(course_A)
        sem_B = self._get_semester_of_course(course_B)

        if not (sem_A and sem_B):
            if not sem_A:
                print(f"{course_A} not in plan.")
            if not sem_B:
                print(f"{course_A} not in plan.")
            return

        if sem_A.name == sem_B.name:
            print(f"{course_A} and {course_B} are both already in {sem_A.name}")
            return

        if not(sem_B.get_type() in COURSE_INFO[course_A][SEM_OFFERED]
           and sem_A.get_type() in COURSE_INFO[course_B][SEM_OFFERED]):

            if sem_B.get_type() not in COURSE_INFO[course_A][SEM_OFFERED]:
                print(f"{course_A} not offered in {sem_B.get_type()} ")

            if sem_A.get_type() not in COURSE_INFO[course_B][SEM_OFFERED] :
                print(f"{course_A} not offered in {sem_B.get_type()} ")
            return

        sem_A.remove_course(course_A)
        sem_B.remove_course(course_B)
        sem_A.add_courses(course_B)
        sem_B.add_courses(course_A)

    def get_missing_prerequisites(self) -> dict[str, str]: #FIXME Account for WHEN prerequisites are taken.
        missing_prereqs_dict = {}
        course_list = self._get_course_list()
        for course in course_list:
            missing_prereqs_dict[course] = []
            if not COURSE_INFO[course][PREREQ]:
                continue
            for prereq_list in COURSE_INFO[course][PREREQ]:
                if not set(prereq_list).intersection(set(course_list)):
                    missing_prereqs_dict[course].append(prereq_list)
        return {course: missing_prereqs for course, missing_prereqs in missing_prereqs_dict.items() 
                if missing_prereqs}

    def get_delayed_prerequisites(self) -> dict[str, tuple[str]]:
        pass   

    def any_incompatiblities(self) -> bool:
        for sem in self.semesters:
            if sem.get_incompatibilities():
                return True
        return False
    
def main():
    plan = initialise_my_plan() # Just a function that creates a new Plan object and uses add_course() method to add all my courses.
                                # I did this to keep my courses (≖_≖ ) secret ( ≖_≖)
    missing_prereqs = plan.get_missing_prerequisites()
    if missing_prereqs:
        pprint(missing_prereqs)
        if not input("Open all missing prerequisite course profiles? [y/n] ").lower() == 'y':
            return
        first_course = tuple((missing_prereqs.values()))[0][0][0]
        webbrowser.open(f"{URL_BASE}{first_course}", 1)
        for missing_prereqs_layered_list in missing_prereqs.values():
            for list in missing_prereqs_layered_list:
                for course in list:
                    if course != first_course:
                        webbrowser.open(f"{URL_BASE}{course}")
                        
        return  
    print("All prerequisites met!!!")



if __name__=='__main__':
    main()