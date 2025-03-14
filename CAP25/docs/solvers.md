# Overview

In *backend* directory, we have kept different versions of our solvers for considerations of different constraint priorities.

Currently there exists two versions of our solver, both of which maximizes the team affinity of the set of all teams by minimizing the min team score in that set.

1. Dot Product of Skill Abilities
   * Makes assignments based on individual fitness to a group.
2. Company Neediness
   * Makes assignments based on collective skillset to a group

---

# Preprocessing

*Data Structures to Setup*

1. List of student objects

```
 student = {
        "name": row["Name"],
        "eid": row["EID"],
        "skill_set": # skillNumber : individual rating
    }
```

2. List of project objects

```jsx
 project = {
        "name": row["Project_ID"],
        "skill_req": # skillNumber : project neediness

```

3. Team Allocation object (example 2D numpy array shown below)

|           | Project 1 | Project 2 | Project 3 |
| --------- | --------- | --------- | --------- |
| Student 1 | TRUE      |           |           |
| Student 2 |           | TRUE      |           |
| Student 3 |           |           | TRUE      |
| Student 4 | TRUE      |           |           |
| Student 5 |           |           | TRUE      |
| Student 6 |           | TRUE      |           |

TRUE denotes assignment between student and project. A student can only be assigned to one project, and team sizes are also constrained.


*CP-Model at a High-Level glance*

We implement the following decision variables:

```jsx
min_goodness
team_goodness_list
team_allocation_object
```

And the following constraint:

```jsx
model.AddMinEquality(min_v, team_goodness_list) 
```

Now, we only change the definition of *goodness* between the solvers based on desired constraints.

---

# Solver 1 - Dot Product of Skill Abilities

Optimizing min team goodness by individual affinity towards group project

```jsx
Project Beta: [3, 3, 3, 5, 3, 3]
Students A to I: [3, 3, 3, 3, 3, 3]	     DotProduct(any student A to I, Z)  = 61 affinity
Student Z: [2, 2, 2, 5, 2, 2]		         DotProduct(student 10, Z) = 55 affinity

Student Z would NOT be selected, despite Project Beta rating a much higher need value for a skill possesesd by Student Z
```

---

# Solver 2 - Company Neediness

Optimizing min team goodness by scaling collective group skill vector by dividing it with the project’s skill rating (project neediness)

```jsx
skill_vector = [10,5]
group_need = [3,2]
scaled_skill_vector = [3.3, 2.5]
```

tag: TODO, Unsure on lcm functionality within this solver

# Basics for SAT Solver

We implemented Google OR-Tools as the solver for the SAT problems. Here is the Example provided by google:

https://developers.google.com/optimization/cp/cp_example

The three most important thing to note in the solver are:

 - Add constraint needed for a legal solution
 - Add objectives function to maximize the utility
 - Always solve for linear problem

## Constraint addition

As we created the variable object, we can treat them as normal integer values like:

```python
x = model.new_int_var(0, 10, "x")
y = model.new_int_var(0, 10, "y")
z = x + y
```

In the implementation of solver, we stored these variable value into the np array to utilize vector operation like dot product and so.

Then you could add constraints using various relation like inequality and min value:

```python
model.add(2 * x+ 3 * y <= z)
model.addMinEquality(z, [x, y])
```

## Utility function

Basically you want to set a variable as the value to maximize or minimize in the solver. Like:

```python
model.maximize(z)
model.maximize(x + y)
```

## Linearity of problem

Since OR tools is just a linear solver, it cannot take in floating coeeficient and you cannot multiply one variable to another. That would make the problem quadratic. So use some trick to work around it.
