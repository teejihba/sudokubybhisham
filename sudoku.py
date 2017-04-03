#   Sudoku Solver 
#	Author : Bhisham Kumar
#		   : Abhijeet Ankush (Some people just show that they are trying to help)
#		   : Date 2-Apr-2017
#
#
import os
import itertools

# Domain of the variables
domain = [list(range(1,10)) for i in range(81)]  
# a variable for keeping track of the assigned variables
assigned = [False for i in range(81)]
# 3 X 3 groups
groups = [[0,1,2,9,10,11,18,19,20]     , [3,4,5,12,13,14,21,22,23]    , [6,7,8,15,16,17,24,25,26],
		  [27,28,29,36,37,38,45,46,47] , [30,31,32,39,40,41,48,49,50] , [33,34,35,42,43,44,51,52,53],
		  [54,55,56,63,64,65,72,73,74] , [57,58,59,66,66,68,75,76,77] , [60,61,62,69,70,71,78,79,80]]

# Neighbours of the all the 81 variables
neighbours = [set() for i in range(81)]

# Initialize neighbous of all the variables
for i in range(9):
	for j in range(9):
		for p in range(9):
			neighbours[9*i + j].add(9*i + p) # Neighbours in the horizontal line
			neighbours[9*i + j].add(j + 9*p) # Neighbours in the vertical line
		
# Add the neighbours within a 3 X 3 group
for elem in groups:
	for items in elem:
		for item in elem:
			neighbours[items].add(item)


# Initial Configuration
inputFile = open("input.txt","r")
counter = 0
for lines in inputFile.readlines():
	if(lines != ' \n') : 
		val = int(lines.strip())
		domain[counter] = [val]
	counter += 1
# Remove the self as a neighbour from the Neighbours
for i in range(81): neighbours[i].remove(i)
		 
# For solving this CSP Arc Consistency Algorithm (AC3) is used
# Input  : X set of variables here we use 1 to 81 implicitly
#		 : D set of domains of the variables which is [1,2,3,4,5,6,7,8,9]  initially
# 		 : C set of binary constraints of the problem or all the edges of the constraint graph .
#		   Here neighbours represent all the edges as well as constraints
# Output : Returns false if the problem is incosistent else true
#		   It also constrains the domains. If all the variables' domain become singleton
#          then that is the solution .

def revise(X,Y):
	revised = False
	for x in domain[X]:
		if not True in [ x!=y for y in domain[Y]]:
			domain[X].remove(x)
			revised = True
	return revised

def AC3():
	queue = []
	for x in range(81):
		for y in neighbours[x]:
			queue.append((x,y))

	while len(queue) > 0:
		(x,y) = queue.pop()
		if revise(x,y):
			if len(domain[x]) == 0 : return False
			for z in neighbours[x].difference({y}):
				queue.append((z,x))
	return True

def isComplete(assignment):
	return not (False in assigned)

# Minimum remaining variable heuristic
def select_unassigned_variable():
	temp = []
	for var in range(81):
		if not assigned[var]:
			temp.append(len(domain[var]))
	return min(range(len(temp)) , key = temp.__getitem__) # index of the variable with min size
# Least Constraining Value heuristic
def order_domain_values(var,assignment):
	temp = [] # indexes of values will be stored 
	for val in assignment[var] :
		counter = 0 # counter for number of times val constrains its neighbours domain
		for n in neighbours[var]:
			if (not assigned[n]) and ( True in (val == x) for x in assignment[n] ) :
				counter += 1
		temp.append(counter)
	return sorted(range(len(temp)) , key = temp.__getitem__)

def is_consistent_assignment(val,var,assignment):
	for n in neighbours[var]:
		if  assigned[n] and val == assignment[n][0] : return False
	return True

def backtrack(assignment):
	if isComplete(assignment) is True : return assignment
	var = select_unassigned_variable() 
	for indexes in order_domain_values(var,assignment):
		val = assignment[var][indexes]
		if is_consistent_assignment(val,var,assignment):
			return True



if AC3() is True:
	for d in domain : print(d) 
else:
	print("Inconsistent")

assigned = [len(d)==1 for d in domain]


