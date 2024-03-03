import pandas

Students = {}

DEBUG = True

HARD_REQUIREMENTS = 10

"""
For the future:
- Code a way to check for NaN values in any part of the excel file and assign them 
    default values. Different sections may have different default values.
- For front-end survey when asking students, either require students to answer with
the correct data type or assign a default value to it when sending it to database or input
excel file.
- Standardize student responses. Give front-end survey to students after company filled their
    respective survey.
"""


class Student:
    def __init__(self, eid, name, gpa, honors, sp, focus, nda, ip,
                 partner_eid, partner_importance,
                 specs, project_prefs):
        # Student Stats.
        self._EID = str(eid)
        self._name = str(name)
        self._GPA = float(gpa)

        # Whether student wants to be in an honors or SP project. Mutually exclusive.
        self._honors = int(honors)
        self._SP = int(sp)

        # Whether student wants to do software, hardware, or both types of work.
        self._focus = int(focus)  # Hardware(0), Software(1), or Both(2).

        # Whether student wants to sign an NDA or an IP.
        self._NDA = int(nda)  # 0 - No 1 - Yes
        self._IP = int(ip)

        # Each student is initially not assigned to a project.
        self._project_id = ""
        self._is_Assigned = False

        # Student partner they are willing to be with. Maybe for the future.
        # For the future, have partner importance return an integer instead.
        # from 0 to 5 with 0 being not important and 5 being very important.
        self._partner_eid = str(partner_eid)
        self._partner_importance = str(partner_importance)

        # Student comfortability ratings with specifications and preference for projects.
        self._specs = dict(specs)
        self._project_prefs = dict(project_prefs)

        # Insert this student object into the dictionary with the eid as the key.
        Students[eid] = self

        # Maybe include student unique experience for instructor to read just in case?

    # End Student Constructor

    # For debugging. Prints out all relevant values.
    def __str__(self):
        print("===============================")
        print("Student EID: " + self._EID)
        print("Name: " + self._name + " GPA: " + str(self._GPA))
        print("NDA: " + str(self._NDA) + " IP: " + str(self._IP))
        print("Focus: " + str(self._focus))
        print("Honors: " + str(self._honors) + " SP: " + str(self._SP))

        print("Project ID: " + self._project_id)
        print("Is Assigned: " + str(self._is_Assigned))

        print("Partner EID: " + self._partner_eid + " Partner Importance: "
              + self._partner_importance)

        print("Specifications:")
        print(self._specs)
        print("\n")
        print("Project Preferences:")
        print(self._project_prefs)
        print("===============================")

    def get_eid(self):
        return self._EID

    def get_name(self):
        return self._name

    def get_gpa(self):
        return self._GPA

    def get_honors(self):
        return self._honors

    def get_sp(self):
        return self._SP

    def get_focus(self):
        return self._focus

    def get_nda(self):
        return self._NDA

    def get_ip(self):
        return self._IP

    def get_project_id(self):
        return self._project_id

    def get_is_assigned(self):
        return self._is_Assigned

    def get_partner_eid(self):
        return self._partner_eid

    def get_partner_importance(self):
        return self._partner_importance

    def get_specs(self):
        return self._specs

    def get_project_prefs(self):
        return self._project_prefs
    def set_is_assigned(self, state):
        self._is_Assigned = state
    def set_project_id(self, project_id):
        self._project_id = project_id


def __read_student_row(df, df2, row_number):
    # df = grouping.get_csv_sample("Fall_2022_Edit_1.01_Companies.csv")
    specs = {}
    count = 0
    for column_label in df.columns:
        if count >= HARD_REQUIREMENTS:
            specs[str(column_label)] = int(df.at[int(row_number), str(column_label)])

        count = count + 1

    project_prefs = {}

    for project_id in df2.columns:
        project_prefs[str(project_id)] = int(df2.at[int(row_number), str(project_id)])

    Student(df.at[row_number, "EID"],
            df.at[row_number, "Name"],
            df.at[row_number, "GPA"],
            df.at[row_number, "Honors"],
            df.at[row_number, "SP"],
            df.at[row_number, "Hardware, Software, or Both"],
            df.at[row_number, "NDA"],
            df.at[row_number, "IP"],
            df.at[row_number, "Partner_EID"],
            df.at[row_number, "Partner_Importance"],
            specs,
            project_prefs)


# xlsx = read_student_excel("..\..\Samples\CSVs\Fall_2022_Edit_1.04_Students.xlsx")
def __get_num_rows_in_excel(df):
    # count = 0
    # for row_label in df.index:
    #     count = count + 1

    return df.shape[0]


def read_student_excel(filepath, excel):
    xlsx = pandas.ExcelFile(filepath + excel)
    df = pandas.read_excel(xlsx, "Student_Info")
    df2 = pandas.read_excel(xlsx, "Project_Preferences")
    num_rows = __get_num_rows_in_excel(df)
    for num in range(num_rows):
        __read_student_row(df, df2, num)


# read_student_excel("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.04_Students.xlsx")
# for student in Students:
# print(Students[student].__str__())
#
# Studentdb = grouping.get_csv_sample("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.0_Students.csv")
#
# print(Studentdb.info())


# O(N) time. Maybe introduce parallel programming to speed up?
def get_average(column_label):
    sum = 0
    count = 0
    for student in Students:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Students[student].get_specs():
            sum = sum + Students[student].get_specs().get(column_label)
        elif column_label in Students[student].get_project_prefs():
            sum = sum + Students[student].get_project_prefs().get(column_label)
        elif column_label == "GPA":
            sum = sum + Students[student].get_gpa()
        elif column_label == "Hardware, Software, or Both":
            sum = sum + Students[student].get_focus()
        elif column_label == "NDA":
            sum = sum + Students[student].get_nda()
        elif column_label == "IP":
            sum = sum + Students[student].get_ip()
        elif column_label == "Honors":
            sum = sum + Students[student].get_honors()
        elif column_label == "SP":
            sum = sum + Students[student].get_sp()
        count = count + 1

    average = sum / count
    if DEBUG:
        txt = "The average value of " + column_label + " is {}."
        print(txt.format(average))
    return average


def get_all_averages(df):
    for column in df.columns():
        get_average(column)


# O(N) time. Maybe introduce parallel programming to speed up?
def get_frequency(column_label, value):
    int_value = int(value)
    count = 0
    for student in Students:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Students[student].get_specs():
            if Students[student].get_specs().get(column_label) == int_value:
                count = count + 1
        elif column_label in Students[student].get_project_prefs():
            if Students[student].get_project_prefs().get(column_label) == int_value:
                count = count + 1
        elif column_label == "Hardware, Software, or Both":
            if Students[student].get_focus() == int_value:
                count = count + 1
        elif column_label == "NDA":
            if Students[student].get_nda() == int_value:
                count = count + 1
        elif column_label == "IP":
            if Students[student].get_ip == int_value:
                count = count + 1
        elif column_label == "Honors":
            if Students[student].get_honors() == int_value:
                count = count + 1
        elif column_label == "SP":
            if Students[student].get_sp() == int_value:
                count = count + 1
    if DEBUG:
        txt = "The frequency of {} for " + column_label + " is {}."
        print(txt.format(value, count))
    return count


def sort_projects(column_label, max_value):
    col_str = str(column_label).lower()
    ordered_list = []
    for num in range(0, max_value + 1):
        for student in Students:
            # print(Projects[project].get_tech_cores().get(column_label))
            if column_label in Students[student].get_specs():
                if Students[student].get_specs().get(column_label) == num:
                    ordered_list.append(Students[student].get_project_id())
            elif column_label in Students[student].get_project_prefs():
                if Students[student].get_project_prefs().get(column_label) == num:
                    ordered_list.append(Students[student].get_project_id())
            elif column_label == "Hardware, Software, or Both":
                if Students[student].get_hardware() == num:
                    ordered_list.append(Students[student].get_project_id())
            # Maybe find another way to sort GPA. However, it is already sorted in file.
            elif column_label == "Honors":
                if Students[student].get_honors() == num:
                    ordered_list.append(Students[student].get_project_id())
            elif column_label == "NDA":
                if Students[student].get_nda() == num:
                    ordered_list.append(Students[student].get_project_id())
            elif column_label == "IP":
                if Students[student].get_ip == num:
                    ordered_list.append(Students[student].get_project_id())
            elif column_label == "SP":
                if Students[student].get_sp() == num:
                    ordered_list.append(Students[student].get_project_id())

    return ordered_list
