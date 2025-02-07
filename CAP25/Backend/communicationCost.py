# CommunicationCost.py
# The set of students encompasses all students who possess any skill required by the project
# Start group allocation by selecting skill with the lowest support
# Select next based on (number of applicable skills possessed by student) and (students communication cost with other students)
    # - ratio will be modified after goodness of fit is implemented

import re
from datetime import datetime

"""
    Function will take in an .ics file and parse it to return an events list which will be passed to the student struct
     -entries will be a tuple of {dtstart, dtend} 
"""
def parse_ics(file_path):
    events = []
    event = {}
    #with open(file_path, 'r') as f:
        #for line in f:
   
        

"""
  Had to redo function:
        - originally was going to just parse it and create a list of str-type events, but its hardrer to compare with ordinal data
        - so instead i plan to use a 5 wide and 48 long matric to represent the days of the week and the hours of the day at 30 minute intervals
        - if a student has a class at that type i will input a one into that time and day in the matrix
        - then use numpy and use element wise multilpication
        - then use a pandas dataframe to count the number of ones in the resultant matrix
"""
def calculateCost():
    pass