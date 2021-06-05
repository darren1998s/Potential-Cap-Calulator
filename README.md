# Potential-Cap-Calulator
A simple calculator to help determine a range of potential cumulative average points (CAP) in NUS after given ranges of grade per module

It also has a built in function to calculate a range of potential CAP you need to hit for future semesters as well.

CON_GRADE_DICT variable is a dictionary which contains all modules you have used and their actual grade in the transcript (post S/U). Key is letter grade, value is another dictionary with corressponding number grade (5 for A/A+, 4.5 for A-...) with this nested dictionary's value being a list of the module codes. 

POTENTIAL_GRADE_DICT variable is a dictionary with key as module code and value as a list of range of values you feel you would achieve in that module (be more liberal).
