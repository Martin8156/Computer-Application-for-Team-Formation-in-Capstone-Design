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

Note: Application was tested on Python 3.13.2

# Getting Started (macOS)

- Install Node.js via Homebrew
- Clone the repository
- Go to CAP25 root direcotry
- Download JavaScript dependencies
- On mac, create a venv and download dependencies from requirements.txt file. For ease of use, the debug.sh script will do this for you.
- Run the start.sh script to run the backend server in the background and the frontend in the foreground on the same terminal.

TLDR

In a macOS terminal:

1. /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. brew install node

In root directory of repository:

1. cd CAP25
2. npm install				# to install JavaScript dependencies
3. ./debug.sh				# to create venv and download dependencies from requirements.txt
4. source venv/bin/activate 	# to activate venv
5. ./start.sh					# to run application

# Current Issues

- Displaying goodness of fit
