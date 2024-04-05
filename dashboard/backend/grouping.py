import os
import pandas as pd
import numpy as np
import random
import project as proj
import student as stud


# Input: value to modified and the weights to modify them
# Output: The weighted product
def apply_weights(value, weights=[0, .5, 1, 1.5, 2]):
    return value * weights[value - 1]


# Function: Gets a project's students and calculates the average skill level of all students involved
# for all specifications.
# Input: Project and variable weights
# Output: Spec Dictionary with the absolute difference of the group spec requirement and the group average
def specification_avg(project, weights=[0, .5, 1, 1.5, 2]):
    student_set = project.get_students()
    avg_spec_dict = {}
    num_students = len(student_set)

    if(num_students == 0):
        largestPossibleValue = max(weights) * 6
        return largestPossibleValue

    for spec in project.get_specs():
        sum = 0
        for student in student_set:
            value = stud.Students[student].get_spec(spec)
            sum += apply_weights(value, weights)

        avg = sum / num_students

        weightedProjPref = apply_weights(project.get_spec(spec), weights)

        difference = np.absolute(weightedProjPref - avg)

        avg_spec_dict[spec] = difference

    return avg_spec_dict


# Input: project with members
# Output: average of the averages - the projects desired value for each specification
# Note: A group that satisfies the desired specifications of the project has a score of 0
def satisfaction_score(project, weights=[0, .5, 1, 1.5, 2]):
    avg_spec_dict = specification_avg(project, weights)
    value = 0
    for val in avg_spec_dict.values():
        value += val

    score = value / len(avg_spec_dict)

    return score



# Has to be run first
def init_students_and_projects(student_filepath, project_filepath, student_excel, project_csv):
    # Initialize both dictionaries. Read both files.
    stud.read_student_excel(student_filepath, student_excel)
    proj.read_projects_csv(project_filepath, project_csv)



# Input: Unsorted dictionary of numbers
# Output: Sorted dictionary of numbers from least to greatest
def sort_dicts(unsorted_dict):
    copy = dict(unsorted_dict.copy())
    sorted_dict = {}
    while (len(copy) != 0):
        lowest_value = 10.99
        lowest_key = ""
        for entree in copy:
            if copy[entree] < lowest_value:
                lowest_value = copy[entree]
                lowest_key = entree

        sorted_dict[lowest_key] = copy.pop(str(lowest_key))

    return sorted_dict


# The function ranks projects from each student's desire to be in that project from worst to best.
# Input: Dictionary of students and projects and weights for variables
# Output: A list of projects ids from the worst ratio to the best
def project_popularity(weights):
    popularity_list_int = []
    popularity_list_str = []
    is_sorted_in_str = []

    # All arrays are length of the number of projects.
    for i in range(len(proj.Projects)):
        popularity_list_int.append(0)
        popularity_list_str.append("")
        is_sorted_in_str.append(False)

    # Get popularity. Add up all student's ratings.
    for student in stud.Students.values():  # Gets student objects
        index = 0

        for pref in student.get_project_prefs():  # Gets each student object's project preference list
            weightedPref = apply_weights(student.get_project_prefs().get(pref), weights)
            proj.Projects[pref].add_popularity(weightedPref)
            popularity_list_int[index] += weightedPref
            index += 1
    popularity_list_int.sort()


    # At this point, the popularity numbers have been sorted.
    # Compare scores in integer list with score assigned to each project in Projects dictionary. If they are equal,
    # assign that project's string to it's already sorted index.
    for group in proj.Projects:

        for index in range(len(popularity_list_int)):
            if (proj.Projects[group].get_popularity() == popularity_list_int[index]
                    and is_sorted_in_str[index] is False):
                popularity_list_str[index] = group
                is_sorted_in_str[index] = True
                break


    return popularity_list_str


# Input: A project with members
# Output: The summed up cost
# Notes: Cost is just a sort of inverse preference rank (6 - project pref = cost)
def total_cost_calc(project):
    student_set = project.get_students()
    projectID = project.get_project_id()
    sum = 0
    for student in student_set:
        cost = 6 - stud.Students.get(student).get_project_prefs().get(projectID)
        sum = sum + cost

    return sum


# The func divides the score by the total cost
# Input: A project with members and weights
# Output: Product of the score and total cost (larger number worse)
# Notes: Cost is just a sort of inverse preference rank (6 - project pref = cost)
def benefit_pref_analysis(project, weights):
    score = satisfaction_score(project, weights)
    totalCost = total_cost_calc(project)
    return (score*totalCost)


# Input: ID of project and student to be added as well as weights
# Output: Score of the group if the student was added
# Notes: Temporarily add student to group, get score, and remove student before returning score
def check_assignment(projectID, studentID, weights):
    if proj.Projects[projectID].check_all(stud.Students[studentID]) is True:
        if len(proj.Projects[projectID].get_students()) != proj.MAX_STUDENTS_IN_PROJECT:
            proj.Projects[projectID].add_student(studentID)
            score = benefit_pref_analysis(proj.Projects.get(projectID), weights)
            proj.Projects[projectID].del_student(studentID)

    else:
        score = 100

    return score


# Input: ID of project, set of students not yet assigned, weights for scores
# Output: No output
# Notes: The best student should be removed from the set and assigned to ID
def assign_best_student(projectID, unassignedStudIDs, weights):
    # ID of student to be added and score (better if closer to 0)
    currentBestID = ""
    currentBestScore = 100

    for targetStudent in unassignedStudIDs:
        scoreToCheck = check_assignment(projectID, targetStudent, weights)

        # If better score, switch to better score (should always be a positive number below 5 or 0)
        if (scoreToCheck < currentBestScore):
            # Should always be true the first time
            currentBestID = targetStudent
            currentBestScore = scoreToCheck

    # Remove the assigned ID, assign student to group
    unassignedStudIDs.remove(currentBestID)
    proj.Projects[projectID].add_student(currentBestID)


# Input: weights for ranks
# Output: list of projectIDs from worst to best benefit pref analysis (larger is worse)
def worst_to_best(weights):
    scoresList = []
    dict = {}
    listOfProjIDs = proj.Projects.keys()

    # Get all their scores and shove it in a dict
    for targetID in listOfProjIDs:
        currentScore = benefit_pref_analysis(proj.Projects.get(targetID), weights)
        dict[targetID] = currentScore
        scoresList.append(currentScore)


    # sort values from greatest to least
    scoresList.sort(reverse=True)

    # swap keys and values
    swappedDict = {value: key for key, value in dict.items()}
    sortedIDs = []

    # grab score in order from sorted list, get relevant projID, add to ID list
    for score in scoresList:
        projID = swappedDict.get(score)
        sortedIDs.append(projID)

    return sortedIDs

# Input: projectID with members and weights
# Output: The team member whose removal provides the least to the group
def find_worst_member(projID, weights):

    projOneOGScore = benefit_pref_analysis(proj.Projects.get(projID), weights)

    studentSet = proj.Projects.get(projID).get_students()
    worstStudentID = ""
    # lower is better so start low
    worstScoreChange = -10000

    # remove student, check score difference, add student
    for student in studentSet:
        proj.Projects[projID].del_student(student)
        removedScore = benefit_pref_analysis(proj.Projects.get(projID), weights)
        diff = removedScore - projOneOGScore

        # get the greatest positive number change (bad for group)
        if(diff > worstScoreChange):
            worstStudentID = student
            worstScoreChange = diff

        proj.Projects[projID].add_student(student)

    return worstStudentID

# Input: Take a projectIDI with an assigned student and another projectID with an assigned student
# Output: Return true if the swap provides a benefit (a number closer to 0) for the swap
# Note: Do a check if the NDA and IP are needed or not
def one_sided_swap_check(projOneID, studentOne, projTwoID, studentTwo, weights):

    projOneOGScore = benefit_pref_analysis(proj.Projects.get(projOneID), weights)

    docCheckOne = proj.Projects.get(projOneID).check_all(stud.Students.get(studentTwo))
    docCheckTwo = proj.Projects.get(projTwoID).check_all(stud.Students.get(studentOne))
    isDocOK = docCheckOne and docCheckTwo

    if(isDocOK):

        # swap once to check
        swap_students(projOneID, studentOne, projTwoID, studentTwo)

        postSwapScore = benefit_pref_analysis(proj.Projects.get(projOneID), weights)
        # lower is better
        isSwapBeneficial = postSwapScore < projOneOGScore

        # swap back
        swap_students(projOneID, studentTwo, projTwoID, studentOne)

        return isSwapBeneficial

    else:
        return False


# Input: Take a projectID with an assigned student and another projectID with an assigned student
# Output: Find the change in score for projectOne after the swap
def one_sided_swap_score_change(projOneID, studentOne, projTwoID, studentTwo, weights):

    projOneOGScore = benefit_pref_analysis(proj.Projects.get(projOneID), weights)


    # swap once to check
    swap_students(projOneID, studentOne, projTwoID, studentTwo)

    postSwapScore = benefit_pref_analysis(proj.Projects.get(projOneID), weights)
    # lower is better
    swapDiff = postSwapScore - projOneOGScore

    # swap back
    swap_students(projOneID, studentTwo, projTwoID, studentOne)

    return swapDiff


# Input: Take a projectID with an assigned student and another projectID with an assigned student
# Output: Swaps students
def swap_students(projOne, studentOne, projTwo, studentTwo):
    # remove the students
    proj.Projects[projOne].del_student(studentOne)
    proj.Projects[projTwo].del_student(studentTwo)
    # add the students
    proj.Projects[projOne].add_student(studentTwo)
    proj.Projects[projTwo].add_student(studentOne)

# Input: Filepaths for students and projects as well as their names and the weights for variables
# Output: A satisfactory grouping of students to projects based on their needs, skills, and preferences
# Notes: First does some pre algorithm sorting, then assigns students, and then swaps for better outcomes
# Restriction: (Min members per group)x(projects) must be <= total number of students <= (max members)x(projects)
def group_sort(student_filepath, project_filepath, student_excel, project_csv, weights=[0, .5, 1, 1.5, 2]):
    # 1. Pre Algorithm Setup

    init_students_and_projects(student_filepath, project_filepath, student_excel, project_csv)

    # Decide initial order for the assessment algorithm
    assessmentOrder = project_popularity(weights)

    # 2. Assignment Algorithm - Assign all students to a group

    unassignedStudIDs = set(stud.Students.keys())

    # As long as there are students are not assigned, continue the loop
    while len(unassignedStudIDs) != 0:

        # For the first pass, it is in order of the
        for targetProj in assessmentOrder:
            if len(unassignedStudIDs) != 0:
                assign_best_student(targetProj, unassignedStudIDs, weights)

        assessmentOrder = worst_to_best(weights)


    # 3. Swapping Algorithm - Have groups make positive value trades for X iterations

    # for each projectID, compare to a different project
    for targetProjOne in assessmentOrder:
        
        worstMemberID = find_worst_member(targetProjOne, weights)
        
        validSwap = False
        projectIDToSwap = ""
        studentIDToSwap = ""
        bestScoreChange = 100
        
        for targetProjTwo in assessmentOrder:
            if targetProjOne != targetProjTwo:

                student_set = proj.Projects.get(targetProjTwo).get_students()

                for student in student_set:
                    # checks if the swap helps projOne
                    isGood = one_sided_swap_check(targetProjOne, worstMemberID, targetProjTwo, student, weights)

                    # if the swap is good for projOne, check if the specifcs are better than last change
                    # Remember, the closer the score is to 0 the better
                    if(isGood):

                        scoreChange = one_sided_swap_score_change(targetProjOne, worstMemberID, targetProjTwo, student, weights)

                        if(bestScoreChange > scoreChange):
                            # if the change in score is negative, its better
                            validSwap = True
                            projectIDToSwap = targetProjTwo
                            studentIDToSwap = student
                            bestScoreChange = scoreChange


        if(validSwap):
            swap_students(targetProjOne, worstMemberID, projectIDToSwap, studentIDToSwap)

        assessmentOrder = worst_to_best(weights)


group_sort("..\..\Samples\CSVs\\","..\..\Samples\CSVs\\","Fall_2022_Edit_1.05_Students.xlsx", "Fall_2022_Edit_1.01_Companies.csv")



