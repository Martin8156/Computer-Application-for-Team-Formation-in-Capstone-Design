import os
import pandas as pd
import numpy as np

def get_csv_sample(filepath, sv):
    if os.path.isfile(filepath + csv):
        return pd.read_csv(filepath + csv)
    
def grouping_algo(students, projects):

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

        studentassigned = false

    return finaldb

def group():
    studentdb = get_csv_sample("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.0_Students.csv")
    companydb = get_csv_sample("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.0_Companies.csv")

    return grouping_algo(studentdb, companydb)

def group_stats(groups, students, projects):

    listOfCompanies = groups['Project'].tolist()
    listOfDataFrameMeans = []

    for projectNum in range(len(groups)):

        allMembers = str(groups.loc[projectNum, "Members"]).split()

        tempdf = pd.DataFrame()


        for member in allMembers:
            studentStats = (students.loc[students['EID'] == member]).drop(columns=['Name [Last, First]', 'EID', 'Honors or SP Project?'])
            tempdf = tempdf._append(studentStats)

        listOfDataFrameMeans.append(tempdf.mean(numeric_only=True))

    return listOfCompanies, listOfDataFrameMeans

#group()