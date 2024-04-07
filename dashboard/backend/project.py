import random

import pandas

DEBUG = False

Projects = {}

"""
Excel File Format:
0 - Project ID (String)
1 - Company Name (String)
2 - Project Name (String)
3 - NDA (Int)
4 - IP  (Int)
5 - Hardware Involvement (Int)
6 - Software Involvement (Int)
7+ - Project Specifications (Int) or Null values
"""

HARD_REQUIREMENTS = 7

MIN_STUDENTS_IN_PROJECT = 4
MAX_STUDENTS_IN_PROJECT = 6


class Project:

    def __init__(self, project_id, comp_name, project_title, nda, ip, hw, sw, specs, students):
        self._project_id = str(project_id)  # Each project has a unique project id.
        self._company_name = str(comp_name)
        self._project_title = str(project_title)
        self._NDA = int(nda)  # 1 - Yes 0 - No
        self._IP = int(ip)  # 1 - Yes 0 - No
        self._hardware = int(hw)  # 1 - min 5 - max
        self._software = int(sw)  # 1 - min 5 - max
        self._specs = dict(specs)  # What exactly the project will involve.
        self._students = set(students)  # Students involved in this project.

        self._popularity = 0
        self._project_cost = 0
        self._avg_spec_dict = {}
        self._avg_student_gpa = 0

        # Add Project to list of projects.
        Projects[self._project_id] = self

    # For debugging. Prints out all relevant values.
    def __str__(self):
        print("===============================")
        print("Project ID: " + self._project_id)
        print("Company: " + self._company_name + " Project Name: " + self._project_title)
        print("NDA: " + str(self._NDA) + " IP: " + str(self._IP))
        txt = "Hardware: {} Software: {}\n"
        print(txt.format(self._hardware, self._software))
        print("Specifications:")
        print(self._specs)
        print("\n")
        print("Students:")
        print(self._students)
        print("===============================")

    def get_project_id(self):
        return self._project_id

    def get_company_name(self):
        return self._company_name

    def get_project_title(self):
        return self._project_title

    def get_nda(self):
        return self._NDA

    def get_ip(self):
        return self._IP

    def get_hardware(self):
        return self._hardware

    def get_software(self):
        return self._software

    def get_specs(self):
        return self._specs

    def get_spec(self, name):
        return self._specs.get(name)

    def get_students(self):
        return self._students

    def get_popularity(self):
        return self._popularity

    def set_popularity(self, new_popularity):
        self._popularity = new_popularity

    def add_popularity(self, number):
        self._popularity += number

    def set_specs(self, new_specs):
        self._specs = new_specs

    def set_students(self, new_students):
        self._students = new_students

    def add_student(self, student_eid):
        self._students.add(student_eid)

    def del_student(self, student_eid):
        self._students.remove(student_eid)

    def del_all_students(self):
        self._students.clear()

    def get_num_students(self):
        return len(self._students)

    def check_nda(self, student):
        if self.get_nda() == 1 and student.get_nda() == 0:
            return False
        return True

    def check_ip(self, student):
        if self.get_ip() == 1 and student.get_ip() == 0:
            return False
        return True

    def check_focus(self, student):
        if self.get_software() == 0 and student.get_focus() == 1:
            return False
        elif self.get_hardware() == 0 and student.get_focus() == 0:
            return False
        return True

    def check_all(self, student):
        if self.check_nda(student) is False or self.check_ip(student) is False:
            return False
        return True

    def check_spec(self, student, spec):
        if student.get_specs().get(spec) < self.get_spec(spec):
            return False
        return True

    def check_all_specs(self, student):
        for spec in self.get_specs():
            if self.check_spec(student, spec) is False:
                return False
        return True

    def set_avg_spec_dict(self, new_dict):
        self._avg_spec_dict = new_dict

    def set_avg_student_gpa(self, new_gpa):
        self._avg_student_gpa = new_gpa

    def get_avg_student_gpa(self):
        return self._avg_student_gpa

    def get_avg_spec_dict(self):
        return self._avg_spec_dict

    def get_project_cost(self):
        return self._project_cost

    def set_project_cost(self, new_project_cost):
        self._project_cost = new_project_cost


def __read_project_row(projects_df, row_number):
    specs = {}

    temp = HARD_REQUIREMENTS

    while temp < projects_df.shape[1]:
        specs[str(projects_df.columns[temp])] = int(projects_df.at[int(row_number), str(projects_df.columns[temp])])

        temp += 1

    Project(projects_df.at[row_number, "Project_ID"],
            projects_df.at[row_number, "Company"],
            projects_df.at[row_number, "Project_Title"],
            projects_df.at[row_number, "NDA"],
            projects_df.at[row_number, "IP"],
            projects_df.at[row_number, "Hardware"],
            projects_df.at[row_number, "Software"],
            specs,
            [])


# Call this method to initialize Projects dictionary and read entire Excel file.
# Input: project file + project file's filepath
def read_projects(filepath, excel_file):
    projects_df = pandas.read_excel(filepath + excel_file)

    for num in range(projects_df.shape[0]):
        __read_project_row(projects_df, num)


def get_average(column_label):
    sum_av = 0
    count = 0
    for project in Projects:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Projects[project].get_specs():
            sum_av = sum_av + Projects[project].get_specs().get(column_label)
        elif column_label == "Hardware":
            sum_av = sum_av + Projects[project].get_hardware()
        elif column_label == "Software":
            sum_av = sum_av + Projects[project].get_software()
        elif column_label == "NDA":
            sum_av = sum_av + Projects[project].get_nda()
        elif column_label == "IP":
            sum_av = sum_av + Projects[project].get_ip()
        count = count + 1

    average = sum_av / count
    if DEBUG:
        txt = "The average value of " + column_label + " is {}."
        print(txt.format(average))
    return average


def get_all_averages(df):
    all_avg_dict = {}
    for column in df.columns():
        all_avg_dict[str(column)] = float(get_average(column))
    return all_avg_dict


# O(N) time. Maybe introduce parallel programming to speed up?
def get_frequency(column_label, value):
    int_value = int(value)
    count = 0
    for project in Projects:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Projects[project].get_specs():
            if Projects[project].get_specs().get(column_label) == int_value:
                count = count + 1
        elif column_label == "Hardware":
            if Projects[project].get_hardware() == int_value:
                count = count + 1
        elif column_label == "Software":
            if Projects[project].get_software() == int_value:
                count = count + 1
        elif column_label == "NDA":
            if Projects[project].get_nda() == int_value:
                count = count + 1
        elif column_label == "IP":
            if Projects[project].get_ip == int_value:
                count = count + 1
    if DEBUG:
        txt = "The frequency of {} for " + column_label + " is {}."
        print(txt.format(value, count))
    return count


def sort_projects(column_label, max_value):
    ordered_list = []
    for num in range(0, max_value + 1):
        for project in Projects:
            # print(Projects[project].get_tech_cores().get(column_label))
            if column_label in Projects[project].get_specs():
                if Projects[project].get_specs().get(column_label) == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif column_label == "Hardware":
                if Projects[project].get_hardware() == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif column_label == "Software":
                if Projects[project].get_software() == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif column_label == "NDA":
                if Projects[project].get_nda() == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif column_label == "IP":
                if Projects[project].get_ip == num:
                    ordered_list.append(Projects[project].get_project_id())

    if DEBUG:
        for obj in ordered_list:
            txt = obj + " has value {} for " + str(column_label)
            print(txt.format(Projects[obj].get_tech_cores().get(column_label)))

    return ordered_list


# Gives each project a random amount of students from 4 to 6. This is to test exporting
# Excel file.
def fill_projects_with_students():
    for project in Projects:
        for num in range(random.randint(4, 6)):
            eid = "EID" + str(num + 1)
            Projects[project].add_student(eid)


def print_all_projects():
    # Assume projects Excel file has been read into the Projects dictionary.
    for project in Projects.values():
        print(project.__str__())


# read_projects("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.02_Companies.xlsx")
