import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
import numpy as np
import os
import json

OUTPUT_PATH = "Files/out.json"
COMP_PATH = "Files/Company.csv"
STUD_PATH = "Files/Student.csv"


if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

df_companies = pd.read_csv(COMP_PATH)
df_students = pd.read_csv(STUD_PATH)

df_companies.drop(['Company','Project_Title'], axis=1,inplace=True)
df_students.drop(['EID','GPA', 'Partner_Importance', 'Partner_EID'], axis=1,inplace=True)
col_index = df_students.columns.get_loc('I1')
df_students = df_students.iloc[:, :col_index]

df_companies.drop(['Hardware', 'Software'], axis = 1,inplace=True)
df_students.drop(['Hardware, Software, or Both','Honors','SP'], axis=1,inplace=True)

np_companies = df_companies.iloc[:,1:].fillna(0).astype(int).to_numpy()
np_students = df_students.iloc[:,1:].fillna(0).astype(int).to_numpy()

affinity_matrix = np.dot(np_companies, np_students.T)
np.set_printoptions(threshold=np.inf)
print(affinity_matrix)

n_students = np_students.shape[0]
n_teams = np_companies.shape[0]
n_skills = np_students.shape[1]

model = cp_model.CpModel()

# Decision variables: assignment[(i, t)] is True if student i is assigned to team t.
assignment = {}
for i in range(n_students):
    for t in range(n_teams):
        assignment[(i, t)] = model.NewBoolVar(f"assign_{i}_{t}")

# Each student is assigned to exactly one team.
for i in range(n_students):
    model.Add(sum(assignment[(i, t)] for t in range(n_teams)) == 1)

# Enforce team size constraints: each team must have between 5 and 7 students.
for t in range(n_teams):
    model.Add(sum(assignment[(i, t)] for i in range(n_students)) >= 3)
    model.Add(sum(assignment[(i, t)] for i in range(n_students)) <= 5)

# Calculate the goodness fit for each team.
# Calculate the goodness fit for each team.
team_goodness = {}
affinity_matrix = np.dot(np_companies, np_students.T)
for t in range(n_teams):
    team_goodness[t] = model.NewIntVar(0, 1000000, f"team_goodness_{t}")
    terms = [assignment[(i, t)] * int(affinity_matrix[t][i]) for i in range(n_students)]
    model.Add(team_goodness[t] == sum(terms))

min_goodness = model.NewIntVar(0, 1000000, "min_goodness")

model.AddMinEquality(min_goodness, [team_goodness[t] for t in range(n_teams)])

# Objective: maximize the minimum team goodness.
model.Maximize(min_goodness)

# Solve the model.
solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
solver.log_callback = print
solver.parameters.max_time_in_seconds = 60 * 1
solver.parameters.num_search_workers = max(os.cpu_count() - 1, 1)
status = solver.Solve(model)

with open(OUTPUT_PATH, 'w') as file:
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Minimum Goodness:", solver.Value(min_goodness))
        res = {t: [i for i in range(n_students) if solver.Value(assignment[(i, t)]) == 1] for t in range(n_teams)}
        file.write(json.dumps(res))
    else:
        print("No solution found.")