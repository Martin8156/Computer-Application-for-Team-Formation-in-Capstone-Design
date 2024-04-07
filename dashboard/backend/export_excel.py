import project
import student
import grouping
import os
import openpyxl
from pandas import DataFrame

grouping.group_sort("..\\..\\Samples\\CSVs\\", "..\\..\\Samples\\CSVs\\", "Fall_2022_Edit_1.05_Students.xlsx",
                    "Fall_2022_Edit_1.02_Companies.xlsx")


def output_groups():
    if not os.path.isdir("\\Downloads\\Sorted Projects"):
        os.makedirs("\\Downloads\\Sorted Projects")

    wb = openpyxl.Workbook()
    test_filename = 'Sorted_Groups.xlsx'
    if not os.path.isfile("\\Downloads\\Sorted Projects\\Sorted_Groups.xlsx"):
        wb.save(os.path.join("\\Downloads\\Sorted Projects", test_filename))

    project_list = []
    company_name_list = []
    project_title_list = []
    student_lists = []
    student_nums = []
    avg_gpa = []
    project_cost = []
    popularity = []
    find_avg_gpas()
    find_project_cost()
    find_avg_specs_dict()
    # Goes through the projects in order.
    # At index 0, all project 0's stats are appended onto lists.
    # At index 1, all project 1's stats are appended onto lists.
    # etc. for all projects.
    # Lists are ordered. The order the elements are added will always be the same unless explicitly altered.
    for projects in project.Projects:
        project_list.append(projects)
        company_name_list.append(project.Projects[projects].get_company_name())
        project_title_list.append(project.Projects[projects].get_project_title())
        student_lists.append(project.Projects[projects].get_students())
        student_nums.append(project.Projects[projects].get_num_students())
        avg_gpa.append('{:.2f}'.format(project.Projects[projects].get_avg_student_gpa()))
        project_cost.append(project.Projects[projects].get_project_cost())
        popularity.append(project.Projects[projects].get_popularity())

    dataframe_dict = {'Project ID': project_list,
                      'Company Name': company_name_list,
                      'Project Name': project_title_list,
                      'Students': student_lists,
                      'Number of Students': student_nums,
                      'Avg GPA': avg_gpa,
                      'Project Cost': project_cost,
                      'Popularity': popularity}

    spec_list = list(project.Projects[project_list[0]].get_specs().keys())

    for spec in spec_list:
        temp_list = []
        for group in project.Projects:
            temp_list.append('{:.2f}'.format(project.Projects[group].get_avg_spec_dict().get(spec)))

        dataframe_dict[spec] = temp_list

    df = DataFrame(dataframe_dict)

    df.to_excel("\\Downloads\\Sorted Projects\\Sorted_Groups.xlsx", sheet_name='sheet1', index=False)

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
