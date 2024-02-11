import os
import pandas as pd
import numpy as np

def get_csv_sample(csv):
    if os.path.isfile("..\..\Samples\CSVs\\" + csv):
        return pd.read_csv("..\..\Samples\CSVs\\" + csv)

studentdb = get_csv_sample("Fall_2022_Edit_1.0_Students.csv")
companydb = get_csv_sample("Fall_2022_Edit_1.0_Companies.csv")

print(studentdb)
print(companydb)

def grouping_algo(students, projects):

    mpg = round(len(students)/len(projects))

    finaldb = pd.DataFrame()
    finaldb.loc[:, 'Project'] = companydb.loc[:, 'Project']
    finaldb.loc[:, 'Company'] = companydb.loc[:, 'Company']
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
            finaldb.loc[grouping, 'Members'] = finaldb.loc[grouping, 'Members'] + " " + id

        studentCounter = studentCounter + 1


    return(finaldb)

print(grouping_algo(studentdb, companydb))


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

group_stats(grouping_algo(studentdb, companydb), studentdb, companydb)

# def group_fittness():
#
