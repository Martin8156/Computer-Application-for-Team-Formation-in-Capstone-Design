import os
import pandas as pd
import numpy as np
import project as proj
import student as stud


def get_csv_sample(filepath, csv):
    if os.path.isfile(filepath + csv):
        return pd.read_csv(filepath + csv)


# When sorting GPAs, put NA values at end. When sorting GPA based on integer values, do not
# factor Na into the average gpa.
def grouping_algo(students, projects):
    """
    mpg = round(len(students)/len(projects))

    finaldb = pd.DataFrame()
    finaldb.loc[:, 'Project'] = projects.loc[:, 'Project']
    finaldb.loc[:, 'Company'] = projects.loc[:, 'Company']
    finaldb["Members"] = ""

    studentIDs = students.loc[:, 'EID']
    studentpreferences = students.loc[:, ['EID', 'Hardware, Software, or Both']]
    studentpreferences.set_index('EID', inplace=True)

    ratiowares = projects.loc[:, ['Project', 'Hardware', 'Software']].to_numpy()

    # list of slots in order of the projects in ratiowares
    listofhardwareslots = []
    listofsoftwareslots = []
    totalslotsavailable = []


    for project in range(len(ratiowares)):

        hardwareprio = ratiowares[project][1]
        softwareprio = ratiowares[project][2]
        totalprio = hardwareprio + softwareprio

        hardwareslots = np.round(((hardwareprio/totalprio)/2) * 10)
        softwareslots = 5 - hardwareslots

        listofhardwareslots.append(int(hardwareslots))
        listofsoftwareslots.append(int(softwareslots))
        totalslotsavailable.append(int(softwareslots))




    groupdict = dict()
    unsortedstudentsIDset = set(studentIDs.to_numpy().flatten())

    while len(unsortedstudentsIDset) !=0:

        targetstudentID = unsortedstudentsIDset.pop()
        studentpreference = studentpreferences.loc[targetstudentID][0]
        # 0 means hardware, 1 means software, 2 means no preference

        #studentassigned = false

    return finaldb
    """


def group():
    studentdf = get_csv_sample("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.01_Students.csv")
    companydf = get_csv_sample("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.01_Companies.csv")

    # Project.read_projects_csv(companydf)

    # return grouping_algo(studentdb, companydb)


# Check if a student and a project are compatible.
# Might check for honors or gpa in the future.
def check_base_student_compatibility(project, student):
    if student.get_focus() is 1 and project.get_software() is 0:
        return False
    elif student.get_focus() is 0 and project.get_hardware() is 0:
        return False
    elif student.get_ip() is 0 and project.get_ip() is 1:
        return False
    elif student.get_nda() is 0 and project.get_nda() is 1:
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

def init_students_and_projects(student_filepath, project_filepath, student_excel, project_csv):
    # Initialize both dictionaries. Read both files.
    stud.read_student_excel(student_filepath, student_excel)
    proj.read_projects_csv(project_filepath, project_csv)

def group_sort(student_filepath, project_filepath, student_excel, project_csv):

    init_students_and_projects(student_filepath, project_filepath, student_excel, project_csv)
    # for person in student.Students:
    #    print(student.Students[person].__str__())
    # for group in project.Projects:
    #    print(project.Projects[group].__str__())
    for group in proj.Projects:
        for num in range(4):
            for person in stud.Students:
                if stud.Students[person].get_is_assigned() == False:
                    pass


#group_sort("..\..\Samples\CSVs\\","..\..\Samples\CSVs\\","Fall_2022_Edit_1.04_Students.xlsx","Fall_2022_Edit_1.02_Companies.csv")

