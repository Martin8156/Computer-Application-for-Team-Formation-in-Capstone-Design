import os
import pandas as pd
import numpy as np

def get_csv_sample(csv):
    if os.path.isfile("..\..\Samples\CSVs\\" + csv):
        return pd.read_csv("..\..\Samples\CSVs\\" + csv)

def grouping_algo(students, projects):

    mpg = round(len(students)/len(projects))

    finaldb = pd.DataFrame()
    finaldb.loc[:, 'Project'] = projects.loc[:, 'Project']
    finaldb.loc[:, 'Company'] = projects.loc[:, 'Company']
    finaldb["Members"] = ""

    studentIDs = students.loc[:, 'EID']
    grouping = -1
    studentCounter = 0

    # for grouping in range(len(finaldb)):
    for id in studentIDs:

        if studentCounter % mpg == 0:
            grouping = grouping + 1

        if finaldb.loc[grouping, 'Members'] == "":
            finaldb.loc[grouping, 'Members'] = id
        else:
            finaldb.loc[grouping, 'Members'] = finaldb.loc[grouping, 'Members'] + ", " + id

        studentCounter = studentCounter + 1

    return finaldb

def group():
    studentdb = get_csv_sample("Fall_2022_Edit_1.0_Students.csv")
    companydb = get_csv_sample("Fall_2022_Edit_1.0_Companies.csv")

    return grouping_algo(studentdb, companydb)