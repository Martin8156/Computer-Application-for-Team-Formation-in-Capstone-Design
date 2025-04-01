# UT-Student-Assignment

A computer application for effective and efficient assignment of students to Capstone Design projects

# Updates (2023-2024)

- Added Fall 2023 Document Files (By Nate Stodola on 11/16/2023)
- Added dashboard framework (Gabriel Mount 01/31/24)
- Created a basic pre and post processing for backend (Nate Stodola on 2/11/24)

# Updates (2024-2025)

- Work completed by the FH3 team, under faculty mentor Elizabeth Moliski, exists in CAP25 root directory
- Created working prototype solver

# General Documentation For 2024 - 2025

This is a project for an efficient automated method of assigning students to capstone design projects. We have expanded on the ideas of a previous year work on this project. However, our implementation is separate and uses a unique way of solving the problem

The software runs as a website where users (like professors) can input CSV files with the student needs and the project needs and upload them to the server. The server then runs a solver and returns the matched teams with certain metrics displayed for the user.

# Getting Started

- Clone the repo
- Cd into CAP25 root direcotry
- Run "npm install" to install Node.js/JavaScript dependencies
- On mac, create a venv and  run "pip install -r requirements.txt" to download Python dependencies to your virtual environment
- Enter the command ./start.bat if on windows or ./start.sh if on mac. These scripts will run the backend server in the background and the frontend in the foreground on the same terminal

# Current Issues

- Only one iteration of solver is allowed before program has to be reset. See *global algo_run*
- Constraint on time compatibiltiy of students not set up
