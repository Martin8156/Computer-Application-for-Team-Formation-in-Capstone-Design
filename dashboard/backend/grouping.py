import os
import pandas as pd
import numpy as np
import project
import student

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

    #Project.read_projects_csv(companydf)

    # return grouping_algo(studentdb, companydb)

def group_sort(student_filepath, project_filepath, student_excel, project_csv):

    # Initialize both dictionaries. Read both files.
    student.read_student_excel(student_filepath, student_excel)
    project.read_projects_csv(project_filepath, project_csv)



