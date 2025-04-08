import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
import os
import json
import csv
from fractions import Fraction
from itertools import product

BASE_DIR = "files/"

OUTPUT_PATH = BASE_DIR + "out.json"
OUTPUT_CSV = BASE_DIR + "out.csv"
COMP_PATH = BASE_DIR + "Company.csv"
STUD_PATH = BASE_DIR + "Student.csv"

CONFIG_FILE = "config.json"

with open(CONFIG_FILE) as f:
    config = json.load(f)
    STU_MAP = config["student_mapping"]
    COM_MAP = config["company_mapping"]
    IMP_MAP = config["skill_importance"]
    AVA_LST = config["time_avaliability"]
    GRP_SIZ = config["group_size"]

STU_MAP = {int(k): v for k, v in STU_MAP.items()}
COM_MAP = {int(k): v for k, v in COM_MAP.items()}
IMP_MAP = {k: Fraction(v) for k, v in IMP_MAP.items()}

np.set_printoptions(threshold=np.inf)


def lcm(xs):

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    if len(xs) == 1:
        return xs[0]
    else:
        temp = lcm(xs[1:])
        return xs[0] * temp // gcd(xs[0], temp)


if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

df_companies = pd.read_csv(COMP_PATH)
df_students = pd.read_csv(STUD_PATH)

# get numpy array dimensions
np_companies = df_companies.iloc[:, 3:].astype(int).to_numpy()
np_students = df_students.iloc[:, 2 + len(AVA_LST):].astype(int).to_numpy()
np_available = df_students.iloc[:, 2:2 + len(AVA_LST)].astype(int).to_numpy()

# map company and student skill to updated values
np_companies = np.vectorize(COM_MAP.get)(np_companies)
np_students = np.vectorize(STU_MAP.get)(np_students)


# scale the company skill importance by the mapping

scale_factor = lcm([v.denominator for v in IMP_MAP.values()])
np_companies *= scale_factor

for i, imp in IMP_MAP.items():
    # get the index of column of the df companies
    col_idx = df_companies.columns.get_loc(i) - 3
    np_companies[:, col_idx] //= imp.denominator
    np_companies[:, col_idx] *= imp.numerator

n_students, n_skills = np_students.shape
n_teams = np_companies.shape[0]


# format some data for output

skill_num_to_name = {
    i: skill for i, skill in enumerate(df_students.columns[2 + len(AVA_LST) :])
}

students = []
for index, row in df_students.iterrows():
    student = {
        "name": row["Name"],
        "eid": row["EID"],
        "skill_set": {
            str(i): STU_MAP[int(row[skill])] for i, skill in skill_num_to_name.items()
        },
    }
    students.append(student)

projects = []
for index, row in df_companies.iterrows():
    project = {
        "name": row["Project_ID"],
        "skill_req": {
            str(i): float((COM_MAP[int(row[skill])] * (1 if skill not in IMP_MAP.keys() else IMP_MAP[skill]))) for i, skill in skill_num_to_name.items()
        },
    }
    projects.append(project)

# setting up model constraints and objective

model = cp_model.CpModel()

# Decision variables: assignment[i, t] is True if student i is assigned to team t.

# Create a numpy array to store assignment variables
assignment = np.empty((n_students, n_teams), dtype=object)

for i, t in product(range(n_students), range(n_teams)):
    assignment[i, t] = model.NewBoolVar(f"assign_s{i}_t{t}")

time_slot = np.empty((n_teams, len(AVA_LST)), dtype=object)
for t, (i, time) in product(range(n_teams), enumerate(AVA_LST)):
    time_slot[t, i] = model.NewBoolVar(f"slot_t{t}_time{time}")

# a team has to have 1 time slot available
for t in range(n_teams):
    model.Add(sum(time_slot[t, :]) == 1)

# if a student is assigned to a team where the time is not available to him,
# if student is added to a time slot unavailable to him, then add penalty to the team goodness

for i, t, (j, time) in product(range(n_students), range(n_teams), enumerate(AVA_LST)):
    model.AddImplication(time_slot[t, j], np_available[i, j]).OnlyEnforceIf(
        assignment[i, t]
    )


# setting up constraints of one student can only be assigned to one team
for i in range(n_students):
    model.Add(sum(assignment[i, :]) == 1)

# setting up constraints of team size
for t in range(n_teams):
    model.Add(sum(assignment[:, t]) >= GRP_SIZ['min'])
    model.Add(sum(assignment[:, t]) <= GRP_SIZ['max'])

# setting up constraints of team goodness

# team_goodness = {}
# for t in range(n_teams):
#     team_goodness[t] = model.NewIntVar(0, 1000000, f"team_goodness_{t}")
#     model.Add(team_goodness[t] == np.dot(affinity_matrix[t, :], assignment[:, t]))


global_factor = lcm(np.unique(np_companies))

team_goodness = np.empty(n_teams, dtype=object)
for t in range(n_teams):
    team_goodness[t] = model.NewIntVar(0, 1000000, f"team_goodness_{t}")
    skills = global_factor // np_companies[t, :]
    sum_skill = assignment[:, t] @ np_students * skills

    model.AddMinEquality(team_goodness[t], sum_skill)

min_goodness = model.NewIntVar(0, 1000000, "min_goodness")

model.AddMinEquality(min_goodness, team_goodness)

# Objective: maximize the minimum team goodness.
model.Maximize(min_goodness)


# from assignment directly to json
def assignment_to_json(val, assignment):
    
    team_assignments = {}
    for t in range(n_teams):
        team_assignments[t] = [
            i for i in range(n_students) if val(assignment[i, t]) == 1
        ]
    return team_assignments


def avalibility_to_json(val, time_slot):
    team_availabilities = {}
    for t in range(n_teams):
        for i, time in enumerate(AVA_LST):
            if val(time_slot[t, i]) == 1:
                team_availabilities[t] = time
    return team_availabilities

students
projects

def metric_team(val, assignment):
    score_dist = []
    for t in range(n_teams):
        skill = sum([
            np.array(list(students[i]['skill_set'].values())) for i in range(n_students) if val(assignment[i, t]) == 1
        ])
        project = np.array(list(projects[t]['skill_req'].values()))
        print(min(skill/project))
        score_dist.append(min(skill/project))
    
    return score_dist

print(scale_factor)
print(global_factor)

class TeamFormationCallback(cp_model.CpSolverSolutionCallback):

    def __init__(self, assignment, time_slot):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.assignment = assignment
        self.time_slot = time_slot
        self.best_obj = None

    def on_solution_callback(self):
        cur_obj = self.ObjectiveValue()

        metric_team(self.Value, self.assignment)

        if self.best_obj is not None and cur_obj <= self.best_obj:
            return

        # if self.best_obj is None or cur_obj > self.best_obj:
        self.best_obj = cur_obj

        parsed_assignment = assignment_to_json(self.Value, self.assignment)
        parsed_time_slot = avalibility_to_json(self.Value, self.time_slot)

        output = {
            "students": students,
            "projects": projects,
            "skills": skill_num_to_name,
            "matching": parsed_assignment,
            "time_slot": parsed_time_slot,
        }

        # output to stdout
        # print(json.dumps(output))
        


        # print(cur_obj)

        # output to files
        with open(OUTPUT_PATH, "w") as file:
            json.dump(output, file, ensure_ascii=False, indent=2)

        with open(OUTPUT_CSV, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Team", "Meet time", "Student Names"])
            for t, s in parsed_assignment.items():
                team_name = projects[t]["name"]
                team_time = parsed_time_slot[t]
                student_names = [students[i]["name"] for i in s]
                writer.writerow([team_name, team_time, *student_names])


# Solve the model.
solver = cp_model.CpSolver()
solver.parameters.log_search_progress = False
solver.log_callback = print

# comment out max_time to run for arbitrary time
# solver.parameters.max_time_in_seconds = 60 * 5
solver.parameters.num_search_workers = max(os.cpu_count() - 1, 1)

solution_callback = TeamFormationCallback(assignment=assignment, time_slot=time_slot)

status = solver.SolveWithSolutionCallback(model, callback=solution_callback)
