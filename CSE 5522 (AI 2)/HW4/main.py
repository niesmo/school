# imports
import sys, os
import algo.MOG as algo

# for testing
import numpy as np
import matplotlib.pyplot as plt

# constants
VOWELS = ['iy', 'eh', 'ah', 'uw', 'ow', 'ao', 'ih', 'ey', 'ay', 'ax']
CONST_COLORS = {
  'iy':'blue',
  'eh':'purple',
  'ah':'blue',
  'uw':'red',
  'ow':'green',
  'ao':'green',
  'ih':'black',
  'ey':'yellow',
  'ay':'cyan',
  'ax':'red'
}


"""
This function will read the data with `filename` in the `data` directory and returns it in an array
"""
def readData(filename, dictionary=False):
  
  # define the store function based on what kind of data it is
  if dictionary:
    returnData = {}
    def store(data):
      if not returnData.has_key(data[2]):
        returnData[data[2]] = []

      returnData[data[2]].append({'x':float(data[0]), 'y':float(data[1])})

  else:
    returnData = []
    def store(data):
      returnData.append({'x':float(data[0]), 'y':float(data[1]), 'vowel':data[2]})

  
  # construct the file path
  testFilePath = os.path.join('data', filename)

  # open the test file
  testFile = open(testFilePath)

  # loop over every line
  for line in testFile:
    # parse the data
    data = line.strip().split(' ')

    # store the data
    store(data)

  return returnData


"""
This is the main function that gets for the EM algorithm
This function will return the gaussians that the algorithm calculates
"""
def doExpectationMaximization(data, hiddenVariableCount=2):
  em = algo.EM(data, hiddenVariableCount)

  # initialize the probabilities and the gaussians
  em.initialize()
  it = 1
  while not em.hasConverged():
    # E-STEP
    em.estimate()

    # M-STEP
    em.maximize()

    # increment it
    it += 1

  print "Converged in", it , "iterations"
  return em;


def printReport(report, l):
  errorRate = 0
  for c in report:
    errorRate += report[c]['error'] * report[c]['total']
    print c, report[c]['error'], report[c]['total']
  errorRate /= l

  print "Error Rate: ", errorRate


"""
The main function that is called when this script is ran
"""
def main():
  # get the training data
  trainingData = readData('train.txt', dictionary=True)
  trainingDataPlot = readData('train.txt', dictionary=False)

  # get the test data
  testingData = readData('test.txt', dictionary=False)



  ''' ------------------- QUESTION 1 PART A ------------------- '''
  print 'Question 1 Part A'
  gaussians = algo.calculateGaussians(trainingData)
  vowelProbablity = algo.getClassProbability(trainingData)

  # using the gaussians and the class probabilities, label the test data
  algo.test(testingData, gaussians, vowelProbablity)
  report = algo.getAccuracy(testingData)

  printReport(report, len(testingData))



  ''' ------------------- QUESTION 1 PART B ------------------- '''
  print '\nQuestion 1 Part B'
  for hvc in range(2,6):
    print "\n\nExpectation Maximization With", hvc, "hidden variables"
    em = doExpectationMaximization(trainingData, hvc)

    algo.emTest(testingData, em.gaussians, em.classProbability, vowelProbablity)
    report = algo.getAccuracy(testingData)

    printReport(report, len(testingData));


if __name__ == "__main__":
  main()