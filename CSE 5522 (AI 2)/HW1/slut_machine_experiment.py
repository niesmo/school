import random
import time
import math

'''
 0 -> Bar				3xBar -> 25
 1 -> Bell			3xBell -> 10
 2 -> Lemon			3xLemon -> 4
 3 -> Cherry		3xCherry -> 3
'''

coin_count = 10

def mean(arr):
	return sum(arr)/len(arr)

def median(lst):
	lst = sorted(lst)
	if len(lst) < 1:
		return None
	if len(lst) %2 == 1:
		return lst[((len(lst)+1)/2)-1]
	else:
		return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0


def pull():
	a = my_rand()
	b = my_rand()
	c = my_rand()
	return [a,b,c]

def my_rand():
	r = random.random()
	if(r < 0.25): return 0
	if(r < 0.5): return 1
	if(r < 0.75): return 2
	return 3

def calculate(res):
	# if they are the same
	if(all_the_same(res)):
		if(res[0] == 0):
			return 25
		if(res[0] == 1):
			return 10
		if(res[0] == 2):
			return 4
		if(res[0] == 3):
			return 3

	if(two_cherries(res)):
		return 2

	if(one_cherry(res)):
		return 1

	return 0

def all_the_same(res):
	if(res[0] == res[1] and res[1] == res[2]):
		return True
	return False;

def two_cherries(res):
	if(res[0] == res[1] and res[0] == 3):
		return True
	if(res[0] == res[2] and res[0] == 3):
		return True
	if(res[1] == res[2] and res[1] == 3):
		return True

	return False

def one_cherry(res):
	if(res[0] == 3 or res[1] == 3 or res[2] == 3):
		return True

	return False

''' Run this experiment 100 times '''
number_of_games_played = []
curr_game_count = 0
for i in range(2000):
	
	# Set and Reset game
	coin_count = 10
	curr_game_count = 0

	while coin_count != 0:

		coin_count -= 1
		curr_game_count += 1

		res = pull()

		''' Did we win anything '''
		won = calculate(res)
		coin_count += won

		if coin_count == 0:
			print 'You played: ' , curr_game_count
			number_of_games_played.append(curr_game_count)
			break

		if(curr_game_count > 1000):
			break


print 'Mean: ' , mean(number_of_games_played)
print 'Median: ', median(number_of_games_played)
