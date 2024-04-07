import pandas

Students = {}

DEBUG = False

HARD_REQUIREMENTS = 10


class Student:
    def __init__(self, eid, name, gpa, honors, sp, focus, nda, ip,
                 partner_eid, partner_importance,
                 specs, project_prefs):
        self._EID = str(eid)
        self._name = str(name)
        self._GPA = float(gpa)

        # If student wants to be in a Self-Proposed or Honors project.
        self._honors = int(honors)  # 0 - No 1 - Yes
        self._SP = int(sp)  # 0 - No 1 - Yes

        # Whether student wants to do software, hardware, or both types of work.
        self._focus = int(focus)  # Hardware(0), Software(1), or Both(2).

        # Whether student wants to sign an NDA or an IP.
        self._NDA = int(nda)  # 0 - No 1 - Yes
        self._IP = int(ip)  # 0 - No 1 - Yes

        # Each student is initially not assigned to a project.
        self._project_id = ""

        # Student partner to be with.
        # For the future, have partner importance return an integer instead.
        # from 0 to 5 with 0 being not important and 5 being very important.
        self._partner_eid = str(partner_eid)
        self._partner_importance = str(partner_importance)

        # Student comfortability ratings with specifications and preference for projects.
        self._specs = dict(specs)  # (string: int) = (specification: specification skill)
        self._project_prefs = dict(project_prefs)  # (string: int) = (project id: willingness to join)

        # Insert this student object into the dictionary with the eid as the key.
        Students[eid] = self  # (string: object) = (eid: student)

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

        print("Partner EID: " + self._partner_eid + " Partner Importance: "
              + self._partner_importance)

        print("Specifications:")
        print(self._specs)
        print("\n")
        print("Project Preferences:")
        print(self._project_prefs)
        print("===============================")
        return ""

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

    def get_partner_eid(self):
        return self._partner_eid

    def get_partner_importance(self):
        return self._partner_importance

    def get_specs(self):
        return self._specs

    def get_spec(self, name):
        return self.get_specs().get(name)

    def get_project_prefs(self):
        return self._project_prefs

    def set_project_id(self, project_id):
        self._project_id = project_id


def __read_student_row(students_df, project_prefs_df, row_number):
    specs = {}

    temp = HARD_REQUIREMENTS

    while temp < students_df.shape[1]:
        specs[str(students_df.columns[temp])] = int(students_df.at[int(row_number), str(students_df.columns[temp])])

        temp += 1

    # count = 0
    # for column_label in studentInfoDF.columns:
    #
    #     if count >= HARD_REQUIREMENTS:
    #         specs[str(column_label)] = int(studentInfoDF.at[int(row_number), str(column_label)])
    #
    #     count = count + 1

    project_prefs = {}

    for project_id in project_prefs_df.columns:
        project_prefs[str(project_id)] = int(project_prefs_df.at[int(row_number), str(project_id)])

    Student(students_df.at[row_number, "EID"],
            students_df.at[row_number, "Name"],
            students_df.at[row_number, "GPA"],
            students_df.at[row_number, "Honors"],
            students_df.at[row_number, "SP"],
            students_df.at[row_number, "Hardware, Software, or Both"],
            students_df.at[row_number, "NDA"],
            students_df.at[row_number, "IP"],
            students_df.at[row_number, "Partner_EID"],
            students_df.at[row_number, "Partner_Importance"],
            specs,
            project_prefs)


def read_student_excel(filepath, excel):
    xlsx = pandas.ExcelFile(filepath + excel)

    student_df = pandas.read_excel(xlsx, "Student_Info")
    project_prefs_df = pandas.read_excel(xlsx, "Project_Preferences")

    for num in range(student_df.shape[0]):
        __read_student_row(student_df, project_prefs_df, num)


# O(N) time. Maybe introduce parallel programming to speed up?
def get_average(column_label):
    sum_av = 0
    count = 0
    for student in Students:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Students[student].get_specs():
            sum_av = sum_av + Students[student].get_specs().get(column_label)
        elif column_label in Students[student].get_project_prefs():
            sum_av = sum_av + Students[student].get_project_prefs().get(column_label)
        elif column_label == "GPA":
            sum_av = sum_av + Students[student].get_gpa()
        elif column_label == "Hardware, Software, or Both":
            sum_av = sum_av + Students[student].get_focus()
        elif column_label == "NDA":
            sum_av = sum_av + Students[student].get_nda()
        elif column_label == "IP":
            sum_av = sum_av + Students[student].get_ip()
        elif column_label == "Honors":
            sum_av = sum_av + Students[student].get_honors()
        elif column_label == "SP":
            sum_av = sum_av + Students[student].get_sp()
        count = count + 1

    average = sum_av / count
    if DEBUG:
        txt = "The average value of " + column_label + " is {}."
        print(txt.format(average))
    return average


def get_all_averages(df):
    all_avg_dict = {}
    for column in df.columns():
        all_avg_dict[column] = float(get_average(column))
    return all_avg_dict


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


def print_all_students():
    # Assume projects Excel file has been read into the Projects dictionary.
    for student in Students.values():
        print(student.__str__())


# read_student_excel("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.05_Students.xlsx")
# print_all_students()
