import project
import students_file
import grouping
import os
import openpyxl
from pandas import DataFrame

grouping.group_sort("..\\..\\Samples\\CSVs\\", "..\\..\\Samples\\CSVs\\", "Fall_2022_Edit_1.05_Students.xlsx",
                    "Fall_2022_Edit_1.02_Companies.xlsx")

def output_groups():
    if not os.path.isdir(os.getcwd() + "\\Downloads\\Sorted Projects"):
        os.makedirs(os.getcwd() + "\\Downloads\\Sorted Projects")

    wb = openpyxl.Workbook()
    test_filename = 'Sorted_Groups.xlsx'
    if not os.path.isfile(os.getcwd() + "\\Downloads\\Sorted Projects\\Sorted_Groups.xlsx"):
        wb.save(os.path.join(os.getcwd() + "\\Downloads\\Sorted Projects", test_filename))

    # Lists needed to output. Refer to project file or output for definitions or example, respectively.
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

    # Makes a dictionary out of the above lists. The key is the column and the list is what will
    # be outputted below that column.
    dataframe_dict = {'ID': project_list,
                      'Company': company_name_list,
                      'Project': project_title_list,
                      'EIDs': student_lists,
                      'Students': student_nums,
                      'Avg GPA': avg_gpa,
                      'Cost': project_cost,
                      'Fame': popularity}

    # Make a spec list of all specializations of all projects. For now, assumed the same.
    spec_list = list(project.Projects[project_list[0]].get_specs().keys())

    # For each spec in the spec list, get the avg student skill score for that spec and add it to the list.
    # After all projects had their student averages for one spec found, append the list to the dictionary.
    for spec in spec_list:
        temp_list = []
        for group in project.Projects:
            temp_list.append('{:.2f}'.format(project.Projects[group].get_avg_spec_dict().get(spec)))

        dataframe_dict[spec] = temp_list

    # Convert the dictionary into a dataframe, and then into an Excel file.
    df = DataFrame(dataframe_dict)

<<<<<<< HEAD
    df.to_excel(os.getcwd() + "\\Downloads\\Sorted Projects\\Sorted_Groups.xlsx", sheet_name='sheet1', index=False)
=======
    df.to_excel("\\Downloads\\Sorted_Groups.xlsx", sheet_name='sheet1', index=False)
>>>>>>> dc494b7bd01a54fc910d566deb489a7bf997767f



def find_avg_gpas():
    for group in project.Projects:
        summ = 0
        student_set = project.Projects[group].get_students()
        for stud in student_set:
            summ += students_file.Students[stud].get_gpa()

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
            cost = 6 - students_file.Students[stud].get_project_prefs().get(group)
            total_cost += cost

        project.Projects[group].set_project_cost(total_cost)
