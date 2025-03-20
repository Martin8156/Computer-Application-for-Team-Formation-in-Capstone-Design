# read the csv file and add two randomized cols of whether student avalible
# this is just a file to

import pandas as pd

df = pd.read_csv("Student.csv")
# print(df)

# [99 rows x 35 columns]

# add two randomized cols of whether student available after EID and before the first skill
# the ratio should be 75% available and 25% not available

import numpy as np
np.random.seed(42)  # for reproducibility
df.insert(2, "MW 1:30-3:00", np.random.choice([1, 0], size=len(df), p=[0.75, 0.25]))
df.insert(3, "MW 3:00-4:30", np.random.choice([1, 0], size=len(df), p=[0.75, 0.25]))

# print the updated DataFrame
print(df)

# save the updated DataFrame to a new CSV file
df.to_csv("Student_Time.csv", index=False)