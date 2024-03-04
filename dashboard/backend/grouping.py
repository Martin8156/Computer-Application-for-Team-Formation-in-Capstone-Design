import os
import pandas as pd
import numpy as np
import project as proj
import student as stud


# When sorting GPAs, put NA values at end. When sorting GPA based on integer values, do not
# factor Na into the average gpa.

# Check if a student and a project are compatible.
# Might check for honors or gpa in the future.
def check_base_student_compatibility(project, student):
    if student.get_focus() == 1 and project.get_software() == 0:
        return False
    elif student.get_focus() == 0 and project.get_hardware() == 0:
        return False
    elif student.get_ip() == 0 and project.get_ip() == 1:
        return False
    elif student.get_nda() == 0 and project.get_nda() == 1:
        return False
    else:
        return True


# Check if a specialization is required for the project and if the student is
# comfortable with that specialization. If so, return True. Otherwise, False.
# Like the above compatibility except only for specs. This is because this one
# will be used more often.
def check_spec_compatibility(project, student, spec):
    spec_set = project.get_specs()
    if spec in spec_set and student.get_specs().get(spec) > 3:
        return True
    else:
        return False


def satisfaction_check(project):
    student_set = project.get_students()
    avg_spec_dict = {}
    num_students = len(student_set)
    for spec in project.get_specs():
        sum = 0
        for student in student_set:
            sum += stud.Students[student].get_spec(spec)

        avg = sum / num_students

        difference = project.get_spec(spec) - avg

        avg_spec_dict[spec] = difference

    return avg_spec_dict


def init_students_and_projects(student_filepath, project_filepath, student_excel, project_csv):
    # Initialize both dictionaries. Read both files.
    stud.read_student_excel(student_filepath, student_excel)
    proj.read_projects_csv(project_filepath, project_csv)

def sort_dicts(unsorted_dict):
    copy = dict(unsorted_dict.copy())
    sorted_dict = {}
    while(len(copy) != 0):
        lowest_value = 10.99
        lowest_key = ""
        for entree in copy:
            if copy[entree] < lowest_value:
                lowest_value = copy[entree]
                lowest_key = entree

        sorted_dict[lowest_key] = copy.pop(str(lowest_key))

    return sorted_dict

def group_sort(student_filepath, project_filepath, student_excel, project_csv):
    init_students_and_projects(student_filepath, project_filepath, student_excel, project_csv)
    # for person in student.Students:
    #    print(student.Students[person].__str__())
    # for group in project.Projects:
    #    print(project.Projects[group].__str__())

    # for group_proj in proj.Projects:
    #     for num in range(4):
    #         for person in stud.Students:
    #             if not stud.Students[person].get_is_assigned():
    #                 pass
    #xlsx = pd.ExcelFile(project_filepath + student_excel)
    #student_df = pd.read_excel(xlsx, "Student_Info")
    #proj_prefs_df = pd.read_excel(xlsx, "Project_Preferences")
    #avg_dict_unsorted = proj.get_all_averages(proj_prefs_df)



# group_sort("..\..\Samples\CSVs\\","..\..\Samples\CSVs\\","Fall_2022_Edit_1.04_Students.xlsx",
# "Fall_2022_Edit_1.02_Companies.csv")

init_students_and_projects("..\..\Samples\CSVs\\", "..\..\Samples\CSVs\\", "Fall_2022_Edit_1.04_Students.xlsx",
                           "Fall_2022_Edit_1.01_Companies.csv")

xlsx = pd.ExcelFile("..\..\Samples\CSVs\\" + "Fall_2022_Edit_1.04_Students.xlsx")
student_df = pd.read_excel(xlsx, "Student_Info")
proj_prefs_df = pd.read_excel(xlsx, "Project_Preferences")
avg_dict_unsorted = stud.get_all_averages(proj_prefs_df)
print(sort_dicts(avg_dict_unsorted))

