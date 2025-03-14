import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
import os
import json
import csv
from fractions import Fraction

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
np_students = df_students.iloc[:, 2:].astype(int).to_numpy()

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


n_students, n_skills = np_students.shape
n_teams = np_companies.shape[0]


# format some data for output

skill_num_to_name = {i: skill for i, skill in enumerate(df_students.columns[2:])}

students = []
for index, row in df_students.iterrows():
    student = {
        "name": row["Name"],
        "eid": row["EID"],
        "skill_set": {
            str(i): float(row[skill]) for i, skill in skill_num_to_name.items()
        },
    }
    students.append(student)

projects = []
for index, row in df_companies.iterrows():
    project = {
        "name": row["Project_ID"],
        "skill_req": {
            str(i): float(row[skill]) for i, skill in skill_num_to_name.items()
        },
    }
    projects.append(project)

# setting up model constraints and objective

model = cp_model.CpModel()

# Decision variables: assignment[(i, t)] is True if student i is assigned to team t.

# Create a numpy array to store assignment variables
assignment = np.empty((n_students, n_teams), dtype=object)
for i in range(n_students):
    for t in range(n_teams):
        assignment[i, t] = model.NewBoolVar(f"assign_s{i}_t{t}")

# setting up constraints of one student can only be assigned to one team
for i in range(n_students):
    model.Add(sum(assignment[i, :]) == 1)

# setting up constraints of team size
for t in range(n_teams):
    model.Add(sum(assignment[:, t]) >= 3)
    model.Add(sum(assignment[:, t]) <= 5)

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


class TeamFormationCallback(cp_model.CpSolverSolutionCallback):

    def __init__(self, assignment):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.assignment = assignment
        self.best_obj = None

    def on_solution_callback(self):
        cur_obj = self.ObjectiveValue()

        if self.best_obj is None or cur_obj > self.best_obj:
            self.best_obj = cur_obj

            parsed_assignment = assignment_to_json(self.Value, self.assignment)
            output = {
                "students": students,
                "projects": projects,
                "skills": skill_num_to_name,
                "matching": parsed_assignment,
            }

            # output to stdout
            print(json.dumps(output))

            # print(cur_obj)

            # output to files
            with open(OUTPUT_PATH, "w") as file:
                json.dump(output, file, ensure_ascii=False, indent=2)

            with open(OUTPUT_CSV, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Team", "Student Names"])
                for t, s in parsed_assignment.items():
                    team_name = projects[t]["name"]
                    student_names = [students[i]["name"] for i in s]
                    writer.writerow([team_name, *student_names])


# Solve the model.
solver = cp_model.CpSolver()
solver.parameters.log_search_progress = False
solver.log_callback = print
solver.parameters.max_time_in_seconds = 60 * 5
solver.parameters.num_search_workers = max(os.cpu_count() - 1, 1)

solution_callback = TeamFormationCallback(assignment=assignment)

status = solver.SolveWithSolutionCallback(model, callback=solution_callback)
