import random

import pandas

DEBUG = False

Projects = {}

HARD_REQUIREMENTS = 6
MIN_STUDENTS_IN_PROJECT = 4


class Project:

    def __init__(self, project_id, comp_name, nda, ip, hw, sw, specs, students):
        self._project_id = str(project_id)  # Each project has a unique project id.
        self._company_name = str(comp_name)
        self._NDA = int(nda)  # 1 - Yes 0 - No
        self._IP = int(ip)  # 1 - Yes 0 - No
        self._hardware = int(hw)  # 1 - min 5 - max
        self._software = int(sw)  # 1 - min 5 - max
        self._specs = dict(specs)  # What exactly the project will involve.
        self._students = set(students)  # Students involved in this project.

        self._num_students = 0

        # Add Project to list of projects.
        Projects[self._project_id] = self

    # For debugging. Prints out all relevant values.
    def __str__(self):
        print("===============================")
        print("Project ID: " + self._project_id)
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

    def set_specs(self, new_specs):
        self._specs = new_specs

    def set_students(self, new_students):
        self._students = new_students

    def add_student(self, student_eid):
        self._students.add(student_eid)
        self._num_students += 1

    def del_student(self, student_eid):
        self._students.remove(student_eid)
        self._num_students -= 1

    def del_all_students(self):
        self._students.clear()
        self._num_students = 0


"""
CVS Format:
0 - Project ID (String)
1 - Company Name (String)
2 - NDA (Int)
3 - IP  (Int)
4 - Hardware Involvement (Int)
5 - Software Involvement (Int)
6+ - Project Specifications (Int) or Null values
"""


def __read_project_row(df, row_number):
    # df = grouping.get_csv_sample("Fall_2022_Edit_1.01_Companies.csv")
    specs = {}
    count = 0
    for column_label in df.columns:
        if count >= HARD_REQUIREMENTS:
            specs[str(column_label)] = int(df.at[int(row_number), str(column_label)])

        count += 1

    Project(df.at[row_number, "Project"],
            df.at[row_number, "Company"],
            df.at[row_number, "NDA"],
            df.at[row_number, "IP"],
            df.at[row_number, "Hardware"],
            df.at[row_number, "Software"],
            specs,
            [])


def __get_num_rows_in_csv(df):
    # count = 0
    # for row_label in df.index:
    #     count = count + 1

    return df.shape[0]


# Call this method to initialize Projects dictionary and read entire CSV file.
def read_projects_csv(filepath, project_csv):
    df = pandas.read_csv(filepath + project_csv)
    num_rows = __get_num_rows_in_csv(df)
    for num in range(num_rows):
        __read_project_row(df, num)


# O(N) time. Maybe introduce parallel programming to speed up?
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
    random_eids = set()
    for project in Projects:
        for num in range(random.randint(4,6)):
            eid = "EID" + str(num + 1)
            Projects[project].add_student(eid)



#read_projects_csv("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.01_Companies.csv")
#fill_projects_with_students()
# for project in Projects:
#     print(Projects[project].__str__())