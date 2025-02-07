import pandas as pd
import numpy as np
from ortools.sat.python import cp_model

df_companies = pd.read_csv('Companies.csv')
df_students = pd.read_csv('Students.csv')

df_companies.drop(['Company','Project_Title'], axis=1,inplace=True)
df_students.drop(['EID','GPA', 'Partner_Importance', 'Partner_EID'], axis=1,inplace=True)
col_index = df_students.columns.get_loc('I1')
df_students = df_students.iloc[:, :col_index]

df_companies.drop(['Hardware', 'Software'], axis = 1,inplace=True)
df_students.drop(['Hardware, Software, or Both','Honors','SP'], axis=1,inplace=True)

np_companies = df_companies.iloc[:,1:].fillna(0).astype(int).to_numpy()
np_students = df_students.iloc[:,1:].fillna(0).astype(int).to_numpy()




# Assuming np_students and np_companies are defined as in your notebook:
# np_companies = df_companies.iloc[:,1:].fillna(0).astype(int).to_numpy()
# np_students = df_students.iloc[:,1:].fillna(0).astype(int).to_numpy()

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
team_goodness = {}
affinity_matrix = np.dot(np_companies, np_students.T)
for t in range(n_teams):
    team_goodness[t] = model.NewIntVar(0, 1000000, f"team_goodness_{t}")
    terms = [assignment[(i, t)] * int(affinity_matrix[t][i]) for i in range(n_students)]
    model.Add(team_goodness[t] == sum(terms))

# team_goodness = {}
# for t in range(n_teams):
#     team_goodness[t] = model.NewIntVar(0, 1000000, f"team_goodness_{t}")
#     terms = []
#     for i in range(n_students):
#         # Compute dot product for student i and team t.
#         dot_product = sum(np_students[i][s] * np_companies[t][s] for s in range(n_skills))
#         terms.append(assignment[(i, t)] * dot_product)
#     model.Add(team_goodness[t] == sum(terms))

# Total goodness across all teams.
total_goodness = model.NewIntVar(0, 1000000, "total_goodness")
model.Add(total_goodness == sum(team_goodness[t] for t in range(n_teams)))

# Objective: maximize the total goodness.
model.Maximize(total_goodness)

# Solve the model.
solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

# if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
#     print("Total Goodness:", solver.Value(total_goodness))
#     for t in range(n_teams):
#         team_students = [i for i in range(n_students) if solver.Value(assignment[(i, t)]) == 1]
#         print(f"Team {t}: Students: {team_students}, Goodness: {solver.Value(team_goodness[t])}")
# else:
#     print("No solution found.")