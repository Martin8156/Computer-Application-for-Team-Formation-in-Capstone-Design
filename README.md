# UT-Student-Assignment
A computer application for effective and efficient assignment of students to Capstone Design projects

# Updates (2023-2024)
- Added Fall 2023 Document Files (By Nate Stodola on 11/16/2023)
- Added dashboard framework (Gabriel Mount 01/31/24)
- Created a basic pre and post processing for backend (Nate Stodola on 2/11/24)

# Updates (2024-2025) 
- Created working prototype solver

# General Documentation For 2024 - 2025
This is a project for an efficient automated method of assigning students to capstone design projects. We have expanded on the ideas of a previous year work on this project. However, our implementation is separate and uses a unique way of solving the problem

The software runs as a website where users (like professors) can input CSV files with the student needs and the project needs and upload them to the server. The server then runs a solver and returns the matched teams with certain metrics displayed for the user. 

# Getting Started On Windows
- Clone the repo (Follow instructions here https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- Now from a terminal (e.g. command prompt) navigate to the cloned repo using the cd command
- Follow instructions here to install Node.js (https://nodejs.org/en/download) if you do not already have it installed
- Follow instructions here to install python (https://www.python.org/downloads/) if you do not already have it installed
- You might have to install some other packages using pip (python's package manager)
- To do this use these commands
    - pip install ortools
    - pip install 
- cd into CAP25
- run npm install
- enter the command ./start.bat if on windows or ./start.sh if on mac

# Current Issues
- Need to implement a better optimization that correctly accounts for Professor 
