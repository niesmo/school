# imports
import sys, os
import algo.MOG as algo

# constants
VOWELS = ['iy', 'eh', 'ah', 'uw', 'ow', 'ao', 'ih', 'ey', 'ay', 'ax']


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
def doEstimationMaximization(data):
  em = algo.EM(data, VOWELS)

  # initialize the probabilities and the gaussians
  em.initialize()

  while not em.hasConverged():
    # E-STEP
    em.estimate()

    # M-STEP
    em.maximize()

  return em.gaussians;



"""
The main function that is called when this script is ran
"""
def main():
  # get the training data
  trainingData = readData('train.txt', dictionary=True)

  # get the test data
  testingData = readData('test.txt', dictionary=False)


  ''' ------------------- QUESTION 1 PART A ------------------- '''
  print 'Question 1 Part A'
  gaussians = algo.calculateGaussians(trainingData)
  classProbablity = algo.getClassProbability(trainingData)

  # using the gaussians and the class probabilities, label the test data
  algo.test(testingData, gaussians, classProbablity)
  accuracy = algo.getAccuracy(testingData)

  for c in accuracy:
    print c, 1-accuracy[c]['accuracy'], accuracy[c]['total']
  



  ''' ------------------- QUESTION 1 PART B ------------------- '''
  print '\nQuestion 1 Part B'
  doEstimationMaximization(trainingData)


if __name__ == "__main__":
  main()