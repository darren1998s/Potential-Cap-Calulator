import numpy as np
import itertools as it
import matplotlib.pyplot as plt

############################
#---------CONSTANTS--------#
############################
#To get honours. 160 MCs to graduate
REQ_MC = 160 

#Target Cap you wanna hit
TARGET = 4.5 

#Init this value as 0. We'll do the calculations for this later.
GRADED_MC = 0

#2+4 MCs for GEQ + CFG #Only mods that have the CSU condition + LSM2301
#and you don't want to put in the dictionary
UNGRADED_MC = 10
'''
############################
#--------DICTIONARY--------#
############################
#Edit these as the semesters pass#
#--CONFIRMED GRADES--#
CON_GRADE_DICT = {'A+':{5:['LSM1102','CM1401']}, 'A':{5:['SP2171','SP3172','GES1021']}, 
'A-':{4.5:['ST1232', 'SP2173', "SP2174", "GER1000", 'LSM2232', 'LSM2251', 'CS1010S']}, 
"S":['LSM1105', 'LSM1106', 'GEH1026', 'LSM1306']} 

#--Non-Confirmed Grades--#
GRADE_NUM_DICT = {}

#--Potential Grades--#
POTENTIAL_GRADE_DICT = {'LSM2233': [4.5], 'LSM2191':[4.5],
						'LSM2253': [5], 'GET1020': [4.5], 'SP3175': [5,4.5], 'SP3176': [4.5, 5]}

'''

############################
#--------DICTIONARY--------#
############################
#Edit these as the semesters pass#
#--CONFIRMED GRADES--#
CON_GRADE_DICT = {'B+':{4:['CM1401','CM1401']}, 'B':{3.5:['SP2171']}, 
'A-':{4.5:['ST1232', 'SP2173', "SP2174", "GER1000"]}, 
"S":['LSM1105','LSM1102','CM1401']} 

#--Non-Confirmed Grades--#
GRADE_NUM_DICT = {}

#--Potential Grades--#
POTENTIAL_GRADE_DICT = {'LSM2233': [4,4.5,5], 'LSM2191':[4,4.5,5],
						'LSM2253': [4,4.5,5], 'GET1020': [4,4.5,5]}



#--Update GRADED_MCs and GRADE_NUM_DICT--#
for grade, point_dict in CON_GRADE_DICT.items():
	if grade != 'S':
		for num in point_dict:
			GRADED_MC += len(point_dict[num])*4

			if grade not in GRADE_NUM_DICT:
				GRADE_NUM_DICT[grade] = [num,0]

			GRADE_NUM_DICT[grade][1] += len(point_dict[num])
	else:
		UNGRADED_MC += len(point_dict)*4

#GRADE_NUM_DICT = {'A+': [5, 2], 'A': [5, 1], 'A-': [4.5, 4]} #[GRADE_POINT, NUMBER]


############################
#---------FUNCTIONS--------#
############################

#Input = {'A+': [5, 2], 'A': [5, 1], 'A-': [4.5, 4]}
#Output = {'A+': 10, 'A': 5, 'A-': 18.0}
def DICT_combine(grade_dict):
	new_d = grade_dict.copy()
	for grade, d in grade_dict.items():
		new_d[grade] = d[1]*d[0]
	return new_d

#Input = {'A+': 10, 'A': 5, 'A-': 18.0}, GRADED_MC
#Output = 4.714285714285714
def CAP_CALC(new_DICT,GRADED_MC):
	summation = sum(new_DICT.values())
	return summation*4 / GRADED_MC

#Input = POTENTIAL_GRADE_DICT = {'GES1021': [4.5, 5],'LSM2232': [4, 4.5]}
#Output = [34.0, 36.0, 36, 38.0] = [(4.5*4 + 4*4) , (5*4 + 4*4)...]
def POT_SUMS(POT_DICT):
	allNames = sorted(POT_DICT)
	combinations = it.product(*(POT_DICT[Name] for Name in allNames))
	var = list(combinations)
	for index in range(len(var)):
		var[index] = sum(var[index])*4
	return var

#Input = CURR_CAP, GRADED_MC, POTENTIAL_GRADE_DICT = {'GES1021': [4.5, 5],'LSM2232': [4, 4.5]}
#Output = POTENIAL_CAP_LST = [4.75, 4.65....], GRADED_MC NEW
def new_CAP_CALC(CURR_CAP, GRADED_MC, POTENTIAL_GRADE_DICT):
	summation = CURR_CAP * GRADED_MC
	num_mcs_pot = len(POTENTIAL_GRADE_DICT)*4
	pot_grades_lst = POT_SUMS(POTENTIAL_GRADE_DICT)
	ael = []
	GRADED_MC += num_mcs_pot
	for g in pot_grades_lst:
		v = summation + g
		ael.append(round(v/(GRADED_MC),3))
	return ael, GRADED_MC


############################
#-------CALCULATIONS-------#
############################

#Input = {'A+': [5, 2], 'A': [5, 1], 'A-': [4.5, 4]}
#Output = {'A+': 10, 'A': 5, 'A-': 18.0}
new_DICT = DICT_combine(GRADE_NUM_DICT)

#Input = {'A+': 10, 'A': 5, 'A-': 18.0}, GRADED_MC
#Output = 4.714285714285714
CURR_CAP = (CAP_CALC(new_DICT,GRADED_MC))

#POTENIAL_CAP_LST = [4.75, 4.65....]
POTENTIAL_CAP_LST = np.array((new_CAP_CALC(CURR_CAP, GRADED_MC, POTENTIAL_GRADE_DICT))[0])

#GRADED_MC
GRADED_MC = (new_CAP_CALC(CURR_CAP, GRADED_MC, POTENTIAL_GRADE_DICT))[1]

#Total MCs Taken
TOT_MC_TAKEN = GRADED_MC + UNGRADED_MC

#Total MCs left to take
NUM_MCs_LEFT = REQ_MC - TOT_MC_TAKEN

#-------Target Grade Calculation RANGE-------#
#To obtain the exact range you need, just change the POTENTIAL_GRADE_DICT
#Dictionary to the exact grades you have.
ONE = (TARGET*(REQ_MC/NUM_MCs_LEFT))
TWO = (TOT_MC_TAKEN/NUM_MCs_LEFT)
TARGET_GRADE = ONE - (POTENTIAL_CAP_LST * TWO) 

#--Uncomment below if you only have 1 grade for your mods--#
print(TARGET_GRADE)



##############################
#-------PLOTTING STUFF-------#
##############################
#-----PLOTTING-----#
try:
	fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
	fig.suptitle('Possible CAP & Potential Range of Cap needed for FCH for Y2S1', fontsize = 20)

	#--PLOT POSSIBLE--#
	ax[0].hist(POTENTIAL_CAP_LST, bins = len(POTENTIAL_CAP_LST)//4)
	min_ylim, max_ylim = plt.ylim()
	ax[0].axvline(POTENTIAL_CAP_LST.mean(), color = 'k', linestyle = 'dashed')
	ax[0].text(POTENTIAL_CAP_LST.mean()*1.006, max_ylim*27, f"Mean: {POTENTIAL_CAP_LST.mean():.4f}", fontsize= 15)
	ax[0].plot([4.5]*10, np.arange(0,20,2))
	ax[0].text(4.4, max_ylim*10, f"CAP {4.5}", fontsize= 15, color = 'orange')
	ax[0].set_xlim(4,5)
	ax[0].set_title('Potential Range of Cap (based on Dict)')
	ax[0].grid()

	#--PLOT TO GET--#
	ax[1].hist(TARGET_GRADE, bins = len(TARGET_GRADE)//4)
	min_ylim, max_ylim = plt.ylim()
	ax[1].axvline(TARGET_GRADE.mean(), color = 'k', linestyle = 'dashed')
	ax[1].text(TARGET_GRADE.mean()*1.006, max_ylim*0.85, f"Mean: {TARGET_GRADE.mean():.4f}", fontsize= 15)
	ax[1].plot([4.5]*10, np.arange(0,20,2))
	ax[1].text(4.52, max_ylim*0.4, f"CAP {4.5}", fontsize= 15, color = 'orange')
	ax[1].set_xlim(4,5)
	ax[1].set_title('Potential Range of Cap needed for rest')
	ax[1].grid()
	plt.show()

except:
	print('Give more ranges!')