import project
import student
import grouping
import os
import openpyxl
from pandas import DataFrame


# colors = []

# project.read_projects_csv("..\..\Samples\CSVs\\", "Fall_2022_Edit_1.01_Companies.csv")
# project.fill_projects_with_students()
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
    avg_gpa = []
    project_cost = []
    popularity = []
    avg_spec_dict = []
    find_avg_gpas()
    find_project_cost()
    find_avg_specs_dict()
    for projects in project.Projects:
        project_list.append(projects)
        company_name_list.append(project.Projects[projects].get_company_name())
        student_lists.append(project.Projects[projects].get_students())
        avg_gpa.append(project.Projects[projects].get_avg_student_gpa())
        project_cost.append(project.Projects[projects].get_project_cost())
        popularity.append(project.Projects[projects].get_popularity())
        avg_spec_dict.append(project.Projects[projects].get_avg_spec_dict())
    df = DataFrame({'Projects': project_list, 'Company Name': company_name_list, 'Students': student_lists,
                    'Avg GPA': avg_gpa, 'Project Cost': project_cost, 'Popularity': popularity,
                    'Avg Specs': avg_spec_dict})



    df.to_excel("\Downloads\Sorted Projects\Sorted_Groups.xlsx", sheet_name='sheet1', index=False)

    wb.save(test_filename)


def find_avg_gpas():
    for group in project.Projects:
        summ = 0
        student_set = project.Projects[group].get_students()
        for stud in student_set:
            summ += student.Students[stud].get_gpa()

        avg = summ / len(student_set)
        project.Projects[group].set_avg_student_gpa(avg)


def find_avg_specs_dict():
    for group in project.Projects:
        project.Projects[group].set_avg_spec_dict(grouping.specification_avg(project.Projects[group]))


def find_project_cost():
    for group in project.Projects:
        student_set = project.Projects[group].get_students()
        total_cost = 0
        for stud in student_set:
            cost = 6 - student.Students[stud].get_project_prefs().get(group)
            total_cost += cost

        project.Projects[group].set_project_cost(total_cost)

output_groups()
