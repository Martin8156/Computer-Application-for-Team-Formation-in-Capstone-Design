import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
import numpy as np
import os
import json
import csv

OUTPUT_PATH = "Files/out.json"
COMP_PATH = "Files/Company.csv"
STUD_PATH = "Files/Student.csv"
OUTPUT_CSV = "Files/out.csv"

np.set_printoptions(threshold=np.inf)


if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)

df_companies = pd.read_csv(COMP_PATH)
df_students = pd.read_csv(STUD_PATH)

# get numpy array dimensions
np_companies = df_companies.iloc[:,3:].astype(int).to_numpy()
np_students = df_students.iloc[:,2:].astype(int).to_numpy()


affinity_matrix = np.dot(np_companies, np_students.T)

n_students, n_skills = np_students.shape
n_teams = np_companies.shape[0]


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
    model.Add(sum(assignment[i, t] for t in range(n_teams)) == 1)

# setting up constraints of team size
for t in range(n_teams):
    model.Add(sum(assignment[i, t] for i in range(n_students)) >= 3)
    model.Add(sum(assignment[i, t] for i in range(n_students)) <= 5)

# setting up constraints of team goodness

team_goodness = {}
for t in range(n_teams):
    team_goodness[t] = model.NewIntVar(0, 1000000, f"team_goodness_{t}")
    model.Add(team_goodness[t] == np.dot(affinity_matrix[t, :], assignment[:, t]))

min_goodness = model.NewIntVar(0, 1000000, "min_goodness")

model.AddMinEquality(min_goodness, [team_goodness[t] for t in range(n_teams)])

# Objective: maximize the minimum team goodness.
model.Maximize(min_goodness)

# 定义一个自定义的求解回调类
class TeamFormationCallback(cp_model.CpSolverSolutionCallback):
    
    def __init__(self, assignment, team_goodness, min_goodness, n_students, n_teams):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._assignment = assignment
        self._team_goodness = team_goodness
        self._min_goodness = min_goodness
        self._n_students = n_students
        self._n_teams = n_teams
        self._solution_count = 0
        self._best_objective = None
    
    def on_solution_callback(self):
        current_objective = self.ObjectiveValue()
        
        # 只有当找到更好的解时才打印
        if self._best_objective is None or current_objective > self._best_objective:
            self._best_objective = current_objective
            self._solution_count += 1
            
            # 打印当前分配方案
            team_assignments = {}
            for t in range(self._n_teams):
                team_assignments[t] = [i for i in range(self._n_students) 
                                    if self.Value(self._assignment[(i, t)]) == 1]
            
            team_info = []
            for t, students in team_assignments.items():
                team_info.append(f"  Team {t}: Students {students}")
            
            # turn the team assignments into a json object and print
            print(json.dumps(team_assignments))

# Solve the model.
solver = cp_model.CpSolver()
solver.parameters.log_search_progress = False
solver.log_callback = print
solver.parameters.max_time_in_seconds = 60 * 5
solver.parameters.num_search_workers = max(os.cpu_count() - 1, 1)

solution_callback = TeamFormationCallback(
    assignment=assignment,
    team_goodness=team_goodness,
    min_goodness=min_goodness,
    n_students=n_students,
    n_teams=n_teams
)

status = solver.SolveWithSolutionCallback(model, callback=solution_callback)

res = None

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("Minimum Goodness:", solver.Value(min_goodness))
    res = {t: [i for i in range(n_students) if solver.Value(assignment[(i, t)]) == 1] for t in range(n_teams)}
else:
    print("No solution found.")

# post processing

skills_mapping = {i: skill for i, skill in enumerate(df_students.columns[2:])}

students = []
for index, row in df_students.iterrows():
    student = {
        "name": row['Name'],
        "eid": int(index),  # Ensure eid is an integer
        "skill_set": {str(i): float(row[skill]) for i, skill in skills_mapping.items()}  # Convert NaN to numbers
    }
    students.append(student)

# Format projects
projects = []
for index, row in df_companies.iterrows():
    project = {
        "name": row['Project_ID'],
        "skill_req": {str(i): float(row[skill]) if not pd.isna(row[skill]) else 0.0 
                     for i, skill in skills_mapping.items()}
    }
    projects.append(project)

# Clean the data before writing
formatted_data = {
    "students": students,
    "projects": projects,
    "skills": {str(i): skill for i, skill in skills_mapping.items()},
    "matching": res
}

"Crash the solver if there is any NAN in it instead of clean it"

# formatted_data = clean_nan_values(formatted_data)

# Output the formatted data with error handling
try:
    print(f"Writing results to {OUTPUT_PATH}")
    with open(OUTPUT_PATH, 'w') as file:
        json.dump(formatted_data, file, ensure_ascii=False, indent=2, 
                 default=lambda x: float(x) if pd.isna(x) else x)
    print("Successfully wrote results")

    if res is not None:
        with open(OUTPUT_CSV, 'w', newline='') as csvfile:
            #print(f"current res is {res.items()}")
            writer = csv.writer(csvfile)
            writer.writerow(["Team", "Student IDs"])
            for t in range(n_teams):
                team_name = projects[t]['name']  # Use the name from the projects list
                student_ids = [students[i]['name'] for i in res.get(t, [])]
                writer.writerow([team_name, *student_ids])
        print(f"Successfully wrote matching results to {OUTPUT_CSV}")
except Exception as e:
    print(f"Error writing results: {str(e)}")