import numpy
import math

class EM:
  def __init__(self, data, classes):
    self.data = data
    self.classes = classes

    self.gaussians = {}
    self.softCounts = {} # this is the Ns in the algorithm
    self.probabilityOfClass = {}


  def initialize(self):
    l = len(self.classes)

    # initialize the initial probability of the classes
    # initialize the initial gaussians (mu, sig)
    for c in self.classes:
      self.probabilityOfClass[c] = 1.0/l




    print self.probabilityOfClass

  def estimate(self):
    pass

  def maximize(self):
    pass

  def hasConverged(self):
    return True


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
  if covariance:
    # probability in the x dirction
    varX = gaussian['sx']**2
    fgx = (1/(math.sqrt(2*math.pi*varX)))*math.exp((-1*(point['x'] - gaussian['mx'])**2)/(2*varX))

    # probability in the y direction 
    varY = gaussian['sy']**2
    fgy = (1/(math.sqrt(2*math.pi*varY)))*math.exp((-1*(point['y'] - gaussian['my'])**2)/(2*varY))

    return fgx * fgy

  # we have to use the actual formula for the gaussian distribution for multi variable
  else:
    return None

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
      tempProb[c] = getGaussianProbability(gaussians[c], d)*classProbability[c]

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
    classReport[c]['accuracy'] = float(classReport[c]['correct']) / classReport[c]['total'] 

  return classReport
    
