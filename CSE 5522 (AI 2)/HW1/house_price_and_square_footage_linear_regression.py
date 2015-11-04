'''
Nima Esmaili Mokaram
CSE 5522
'''

import time
import math
from sys import argv


def mean(arr):
	return sum(arr)/len(arr)

def std(arr):
	m = mean(arr)
	ssd = 0

	for num in arr:
		ssd += pow((num - m), 2)

	msd = ssd/len(arr)

	return math.sqrt(msd)


# Getting the file name
script, filename = argv

# Openning the file
m_file = open(filename)


# Read the file and insert them into an array
size = []
price = []

for line in m_file:
	curr_line = line.strip().split('\t')

	# Inserting the data into a variable
	price.append(float(curr_line[0]))
	size.append(float(curr_line[1]))

# --------------------------- PART A ---------------------------
print '------- PART A ---------'
print 'Mean of Price: ', mean(price) 
print 'Mean of Size: ', mean(size)
print

print 'STD of Price: ', std(price)
print 'STD of Size: ', std(size)
print

print 'Min of Price: ', min(price)
print 'Min of Size: ', min(size)
print

print 'Max of Price: ', max(price)
print 'Max of Size: ', max(size)
print




# --------------------------- PART B ---------------------------
def sum_of_mult(arr1, arr2):
	sum = 0;
	for i, num in enumerate(arr1):
		sum += num * arr2[i]
	return sum

def sum_of_squared(arr):
	sum = 0
	for num in arr:
		sum += pow(num,2)
	return sum


N = len(size)
w1 = ((N*sum_of_mult(size, price))-(sum(size)*sum(price)))/((N*sum_of_squared(size))-(pow(sum(size), 2)))
w0 = ((sum(price))-(w1*sum(size)))/N

print "----------- PART B ----------"
print 'W1: ', w1
print 'W0: ', w0

# --------------------------- PART C ---------------------------
# REFERENCE : http://cs229.stanford.edu/notes/cs229-notes1.pdf

print
print "------------ PART C --------------"

# initial values for the w1 and w0
newW1 = w1 + 100
newW0 = w0 + 100

# alpha
alpha = 0.000000001

# epsilon
epsilon = 0.000001

# initial difference
dw1 = 100
dw0 = 100


iterationCount = 0
NN = float(N)

# While the difference is larger than epsilon
while(dw1 > epsilon or dw0 > epsilon):
	#update newW's
	iterationCount += 1
	
	gradiant = 0

	# calculate the gradiant
	for i in range(N):
		gradiant += -(2/NN) * size[i] * (price[i] - ((newW1*size[i]) + newW0)) # b

	# Updatge the weights
	newW0 = newW0 - (alpha * gradiant) 
	newW1 = newW1 - (alpha * gradiant) 

	#update deltas
	dw0 = newW0 - w0
	dw1 = newW1 - w1



print 'Converged in ', iterationCount, ' iterations.'

print 'new W1: ', newW1
print 'new W0: ', newW0	