import numpy
import math
import random

class EM:
  def __init__(self, data, hiddenVariableStateCount, covariance=True):
    self.data = data
    self.classes = data.keys()
    self.hiddenVariables = range(hiddenVariableStateCount) # the array containing the hidden variable classes
    self.covariance = covariance
    self.probabilities = {}
    self.epsilon = 0.001

    self.gaussians = {}
    self.softCounts = {} # this is the Ns in the algorithm
    self.classProbability = {}
    self.logLikelihood = {}
    self.prevLogLikelihood = {}


  '''
  In this function, all the gaussians are initialized to random gaussians
  '''
  def initialize(self):
    tempGaussians = calculateGaussians(self.data)

    # initialize the initial gaussians (mu, sig)
    # and the prior probabilities
    for c in self.classes:
      self.classProbability[c] = {}
      self.gaussians[c] = {}

      for hv in self.hiddenVariables:
        # set the prior probabilities
        self.classProbability[c][hv] = 0.5


        # TODO: you can set the gaussians to have initial value of the global mean and std of that vowel
        # set the gaussians to be random gaussians
        self.gaussians[c][hv] = {
          'mx': tempGaussians[c]['mx'] + random.uniform(-50,50),
          # 'mx':random.uniform(500,3000),

          'sx': tempGaussians[c]['sx'] + random.uniform(-50,50),
          # 'sx':random.uniform(30,400),
          
          'my': tempGaussians[c]['my'] + random.uniform(-50,50),
          # 'my':random.uniform(0,1200),

          'sy': tempGaussians[c]['sy'] + random.uniform(-50,50),
          # 'sy':random.uniform(30,400)
        }

      self.setLogLikelihood(c)

  def estimate(self):
    # for every class
    for c in self.classes:
      self.probabilities[c] = {}
      # for every hidden variable state
      for hv in self.hiddenVariables:
        # the array that holds the probability of that point for class hv
        self.probabilities[c][hv] = []

        # for every data point in this class
        for x in self.data[c]:
          # what is the probability of mixture vowel give the point
          # P(vm|x)
          numerator = getGaussianProbability(self.gaussians[c][hv], x, self.covariance) * self.classProbability[c][hv]
          alpha = 0

          # the normalization step
          for hVar in self.hiddenVariables:
            alpha += (getGaussianProbability(self.gaussians[c][hVar], x, self.covariance))*(self.classProbability[c][hVar])

          self.probabilities[c][hv].append(numerator/alpha)

  '''
  This function will update the different variables of the system
  will update the means and standard stds and also the probabilities of the 
  '''
  def maximize(self):
    for c in self.classes:
      
      sumOfProbabilities = 0
      for mv in self.probabilities[c]:
        # for each points probability
        for d in self.probabilities[c][mv]:
          sumOfProbabilities += d

      # for each mixture
      for mv in self.probabilities[c]:
        # calculate the means and stds
        # The for is to sum the values
        numeratorX = 0
        numeratorY = 0
        denominator = 0

        # for each points probability
        for i, d in enumerate(self.probabilities[c][mv]):
          numeratorX += d*self.data[c][i]['x']
          numeratorY += d*self.data[c][i]['y']
          denominator += d

        self.gaussians[c][mv]['mx'] = numeratorX / denominator
        self.gaussians[c][mv]['my'] = numeratorY / denominator

        # calculate the new std
        numeratorX = 0
        numeratorY = 0

        ax = 0
        ay = 0
        for i, d in enumerate(self.probabilities[c][mv]):
          ax += d * (self.data[c][i]['x']**2) 
          ay += d * (self.data[c][i]['y']**2) 

          # numeratorX += d * (self.data[c][i]['x'] - self.gaussians[c][mv]['mx'])**2 
          # numeratorY += d * (self.data[c][i]['y'] - self.gaussians[c][mv]['my'])**2

        # self.gaussians[c][mv]['sx'] = numeratorX / denominator
        # self.gaussians[c][mv]['sy'] = numeratorY / denominator
        
        self.gaussians[c][mv]['sx'] = math.sqrt((ax/denominator) - ((self.gaussians[c][mv]['mx'])**2))
        self.gaussians[c][mv]['sy'] = math.sqrt((ay/denominator) - ((self.gaussians[c][mv]['my'])**2))

        # update the priors
        # self.classProbability[c][mv] = denominator / len(self.probabilities[c][mv])
        self.classProbability[c][mv] = denominator / sumOfProbabilities

      self.setLogLikelihood(c)

  '''
  will return true if the system has converged
  '''
  def hasConverged(self):
    for c in self.classes:
      if not self.prevLogLikelihood.has_key(c):
        return False

      if abs(self.logLikelihood[c] - self.prevLogLikelihood[c]) > self.epsilon:
        return False

    return True
  
  '''
  This function calculates the log likelihood of the class c for the current iteration
  http://www.micc.unifi.it/seidenari/wp-content/uploads/2010/01/A48-Expectation-Maximization1.pdf -> page 10
  '''
  def setLogLikelihood(self, c):
    totalSum = 0
    for d in self.data[c]:
      localSum = 0
      for hv in self.hiddenVariables:
        localSum += self.classProbability[c][hv] * getGaussianProbability(self.gaussians[c][hv], d, self.covariance)

      totalSum += math.log(localSum)

    # setting the previous log likelihood
    if self.logLikelihood.has_key(c):
      self.prevLogLikelihood[c] = self.logLikelihood[c]

    # setting the new log likelihood
    self.logLikelihood[c] = totalSum;


'''
This function will calculate the gaussians for each class of the data
@param data is a dictionary of classes that each class has all the data for that class

Gaussians are assumed to have diagnol covariance -- treat each dimension separately and then multiply them
'''
def calculateGaussians(data):
  gaussians = {}
  for c in data.keys():
    gaussians[c] = {
      "mx":0, # mu in the x direction
      "sx":0, # sigma in the x direction 
      "my":0, # mu in the y direction
      "sy":0  # sigma in the y direction
    }

    xValues = [d['x'] for d in data[c]]
    yValues = [d['y'] for d in data[c]]
    # calculate the mu's
    gaussians[c]['mx'] = sum(xValues) / len(data[c])
    gaussians[c]['sx'] = numpy.std(xValues)
    gaussians[c]['my'] = sum(yValues) / len(data[c])
    gaussians[c]['sy'] = numpy.std(yValues)

  return gaussians
  

"""
This function will plug the point into the gaussian and return the probability of the point in the gaussian
This value is always between 0 and 1
http://hyperphysics.phy-astr.gsu.edu/hbase/math/gaufcn.html
"""
def getGaussianProbability(gaussian, point, covariance=True):
  varX = gaussian['sx']**2
  varY = gaussian['sy']**2

  if covariance:
    # probability in the x dirction
    fgx = (1/(math.sqrt(2*math.pi*varX)))*math.exp((-1*(point['x'] - gaussian['mx'])**2)/(2*varX))

    # probability in the y direction 
    fgy = (1/(math.sqrt(2*math.pi*varY)))*math.exp((-1*(point['y'] - gaussian['my'])**2)/(2*varY))

    return fgx * fgy

  # we have to use the actual formula for the gaussian distribution for multi variable
  else:
    return (1/(math.sqrt(((2*math.pi)**2)*varX*varY)))*math.exp(-0.5*(((point['x'] - gaussian['mx'])**2)/varX)-(0.5*(((point['y'] - gaussian['my'])**2)/varY)))

"""
This function returns the probability of the each class in the data
=> P(c)
"""
def getClassProbability(data):
  classProbability = {}
  totalCount = 0
  for c in data:
    # set the count of each class
    classProbability[c] = len(data[c])

    # adding to the total count
    totalCount += len(data[c])

  for c in data:
    classProbability[c] /= float(totalCount)

  return classProbability


"""
This function will run through the data (test data) and for each data point calculates based on the gaussians
and the class probabilities, what vowel is the most probable.
"""
def test(data, gaussians, classProbability):
  # for every data point
  for d in data:
    tempProb = {}
    maxProb = {'p':-2, 'label':''} # some `very` small probability
    # for every class
    for c in classProbability:
      # P(c|x) = P(x|c)*P(c) = Gc(x)*P(c) where Gc is the gaussian for class c
      # We dont have to normalize the probability because we are picking the maximum
      tempProb[c] = getGaussianProbability(gaussians[c], d, False)*classProbability[c]

      if tempProb[c] > maxProb['p']:
        maxProb['p'] = tempProb[c]
        maxProb['label'] = c

    d['inferedVowel'] = maxProb['label']

def getAccuracy(data):
  classReport = {}
  for d in data:
    c = d['vowel']

    if not classReport.has_key(c):
      classReport[c] = {'correct':0, 'total': 0}

    if d['vowel'] == d['inferedVowel']:
      classReport[c]['correct'] += 1

    classReport[c]['total'] += 1

  for c in classReport:
    classReport[c]['success'] = float(classReport[c]['correct']) / classReport[c]['total']
    classReport[c]['error'] = 1 - classReport[c]['success']

  return classReport

def emTest(data, gaussians, classProbability, vowelProbability):
  # for every data point
  for d in data:
    tempProb = {}
    maxProb = {'p':float("-inf"), 'label':''} # some `very` small probability
    # for every class
    for c in classProbability:
      tempProb[c] = 0

      for hv in classProbability[c]:

        # We dont have to normalize the probability because we are picking the maximum
        tempProb[c] += getGaussianProbability(gaussians[c][hv], d, False)*classProbability[c][hv]*vowelProbability[c]

      if tempProb[c] > maxProb['p']:
        maxProb['p'] = tempProb[c]
        maxProb['label'] = c

      d['inferedVowel'] = maxProb['label']
