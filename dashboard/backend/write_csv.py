import project
import os
import openpyxl
from pandas import DataFrame
colors = []

project.read_projects_csv("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.01_Companies.csv")
project.fill_projects_with_students()
def output_groups():
    if not os.path.isdir("\Downloads\Sorted Projects"):
        os.makedirs("\Downloads\Sorted Projects")

    wb = openpyxl.Workbook()
    test_filename = 'Sorted_Groups.xlsx'
    if not os.path.isfile("\Downloads\Sorted Projects\Sorted_Groups.xlsx"):
        wb.save(os.path.join("\Downloads\Sorted Projects", test_filename))

    project_list = []
    company_name_list = []
    student_lists = []
    for projects in project.Projects:
        project_list.append(projects)
        company_name_list.append(project.Projects[projects].get_company_name())
        student_lists.append(project.Projects[projects].get_students())
    df = DataFrame({'Projects': project_list, 'Company Name': company_name_list, 'Students': student_lists})
    df.to_excel("\Downloads\Sorted Projects\Sorted_Groups.xlsx", sheet_name='sheet1', index=False)

    wb.save(test_filename)


output_groups()