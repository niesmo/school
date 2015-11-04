# imports
import numpy as np

# Global variables
trainingFilename = "game_attrdata_train.dat"
testingFilename = "game_attrdata_test.dat"
gameTraining = []
gameTesting = []
labelDic = {
  'dow': 0,
  'tod': 1,
  'ttp': 2,
  'mood': 3,
  'fv': 4,
  'kp': 5,
  'ah': 6,
  's': 7,
  'g': 8,
};
answer = 'g'
questions = [q for q in labelDic if not q == answer]

# functions
'''
Data is the dataset as an array of objects
target is the field that we are looking for the probability
'''
def probability(data, target, weights=None):
  # setting the weights to equal values if not passed in
  if weights is None:
    weights = [1.0/len(data)] * len(data);

  dist = {}
  for i, d in enumerate(data):
    if not dist.has_key(d[target]):
      dist[d[target]] = 0

    dist[d[target]] += 1 * weights[i] * len(data)
  for p in dist:
    dist[p] /= float(len(data))
  return dist

'''
givens are formated as such
{
 target1: value1,
 target2: value2,
 .
 .
 .
}
'''
def probabilityGiven(data, target, givens, weights):
  dist = {}
  count = 0
  for i, d in enumerate(data):
    given = True

    for g in givens:
      if not d[g] == givens[g]:
        given = False
        break

    if given:
      count += 1 * weights[i] * len(data)
      if not dist.has_key(d[target]):
        dist[d[target]] = 0
      dist[d[target]] += 1 * weights[i] * len(data)

  for p in dist:
    dist[p] /= float(count)
  return dist;

'''
returns the information gain of the target based on the parent entropy in data
'''
def infoGain(data, target, parentEntropy, weights):
  # setting the weights to equal values if not passed in
  if weights is None:
    weights = [1.0/len(data)]*len(data);

  targetProb = probability(data, target, weights)
  newEntropy = 0
  for c in targetProb:
    newEntropy += entropy(probabilityGiven(data, answer, {target: c}, weights))*targetProb[c]
  
  return parentEntropy - newEntropy;

'''
returns the entropy of the passed probability
'''
def entropy(prob):
  mSum = 0;
  for p in prob:
    mSum += prob[p]*np.log2(prob[p])

  return -1*mSum;

'''
finds the best answer based on the information gain and the entropy of parent
'''
def findBestQuestion(data, questions, entropy, weights=None):
  # setting the weights to equal values if not passed in
  if weights is None:
    weights = [1.0/len(data)]*len(data);

  bestQuestion = None
  tempMax = -1000
  for question in questions:
    temp = infoGain(data, question, entropy, weights)
    
    # print question, temp

    if temp > tempMax:
      tempMax = temp
      bestQuestion = question

  return bestQuestion

'''
classify the data based on the question and using the weights
'''
def classify(data, question, weights=None):
  # setting the weights to equal values if not passed in
  if weights is None:
    weights = [1.0/len(data)]*len(data);

  dist = {}
  for i, d in enumerate(data):
    if not dist.has_key(d[question]):
      dist[d[question]]= {}

    if not dist[d[question]].has_key(d[answer]):
      dist[d[question]][d[answer]] = 0


    dist[d[question]][d[answer]] += weights[i]

  for d in dist:
    normalize(dist[d]);
  
  return dist

def normalize(arg):
  tatal = 0 
  if type(arg) is list:
    total = sum(arg)
    for i, d in enumerate(arg):
      arg[i] /= float(total)

  if type(arg) is dict:
    total = sum(arg.values())
    for d in arg:
      arg[d] /= float(total)

  return arg;


'''
returns the accuracy and error rate of the data
based on the given classification when testing the question
'''
def test(data, classification, question):
  errorCount = 0
  for d in data:
    if classification[d[question]][d[answer]] < 0.5:
      errorCount +=1

  return {
    'errorCount': errorCount,
    'errorRate': errorCount/float(len(data)),
    'correctCount': len(data) - errorCount,
    'correctRate': (len(data) - errorCount)/float(len(data))
  };

def testOne(row, classification, question):
  # print "question: ", question
  # print "row: ", row
  # print "classification: ", classification
  return True if (classification[row[question]][row[answer]] >= 0.5) else False


'''
Returns the average of a classification
'''
def average(classification, question):
  correctCount = 0
  sumProbs = 0
  for d in gameTesting:
    hypothesis = "ApplesToApples" if classification[d[question]]["ApplesToApples"] > 0.5 else "SettersOfCatan"
    if hypothesis == d[answer]:
      correctCount += 1
      sumProbs += classification[d[question]][hypothesis]

  return sumProbs / float(correctCount)

  # initialize the average variable that will be returned
  # mAverage = {}
  # for c in classification:
  #   for f in classification[c]:
  #     mAverage[f] = 0;
  #   break;

  # # calculate the average
  # for f in mAverage:
  #   mAverage[f] = sum([dist[f] for dist in classification.values()])/len([dist[f] for dist in classification.values()])
    
  # return mAverage;


def weightedMajority(classifications, z, bestQuestions):
  errorCount = 0

  for d in gameTesting:

    trueOutcome = {True:0, False:0}
    for i, classification in enumerate(classifications):
      testRes = testOne(d, classification, bestQuestions[i])
      trueOutcome[testRes] += z[i];
     
    # we picked the wrong choice
    if trueOutcome[False] > trueOutcome[True]:
      errorCount+=1

  return {
    'errorCount': errorCount,
    'errorRate': errorCount/float(len(gameTesting)),
    'correctCount': len(gameTesting) - errorCount,
    'correctRate': (len(gameTesting) - errorCount)/float(len(gameTesting))
  };
  

'''
AdaBoost
'''
def adaBoost(data, classify, ensembleCount):
  # initialization of the weights
  weights = [1.0/len(data)] * len(data)
  z = []
  classifications = []
  bestQuestions = []

  for k in range(ensembleCount):
    prob = probability(data, answer, weights)

    rootEntropy = entropy(prob)
    bestQuestion = findBestQuestion(data, questions, rootEntropy, weights)
    classifications.append(classify(data, bestQuestion, weights))

    # print classifications[k]

    # appending the best question to the list of all the question
    bestQuestions.append(bestQuestion);

    # Set the error
    error = 0

    for i, d in enumerate(data):
      # if the guess was wrong
      if classifications[k][d[bestQuestion]][d[answer]] < 0.5:
        error += weights[i]

    for i, d in enumerate(data):
      if classifications[k][d[bestQuestion]][d[answer]] >= 0.5:
        weights[i] *= error/float(1-error)


    normalize(weights)

    z.append(np.log((1-error)/float(error)))

  return weightedMajority(classifications, z, bestQuestions)


# Read in the data
'''
Reading the training data
'''
f=open(trainingFilename,'r')
for line in f:
  parts = line.strip().split(',');
  gameTraining.append({
    'dow': parts[labelDic['dow']],
    'tod': parts[labelDic['tod']],
    'ttp': parts[labelDic['ttp']],
    'mood': parts[labelDic['mood']],
    'fv': parts[labelDic['fv']],
    'kp': parts[labelDic['kp']],
    'ah': parts[labelDic['ah']],
    's': parts[labelDic['s']],
    'g': parts[labelDic['g']]
  });
f.close()

f=open(testingFilename,'r')
for line in f:
  parts = line.strip().split(',');
  gameTesting.append({
    'dow': parts[labelDic['dow']],
    'tod': parts[labelDic['tod']],
    'ttp': parts[labelDic['ttp']],
    'mood': parts[labelDic['mood']],
    'fv': parts[labelDic['fv']],
    'kp': parts[labelDic['kp']],
    'ah': parts[labelDic['ah']],
    's': parts[labelDic['s']],
    'g': parts[labelDic['g']]
  });
f.close()


rootEntropy = entropy(probability(gameTraining, answer))
bestQuestion = findBestQuestion(gameTraining, questions, rootEntropy)
classification = classify(gameTraining, bestQuestion)

# part a
accuracy = test(gameTesting, classification, bestQuestion)
averageOfClassification = average(classification, bestQuestion)
print "PART A\n---------------------------------"
print "Accuracy:   ", accuracy['correctRate']
print "Error Rate: ", accuracy['errorRate']
print "Average probability assigned to the correct class across the test set", round(averageOfClassification, 3)
# print accuracy
print


# part b
print "\nPART B\n---------------------------------"
for k in range(5):
  print "k =", k+2, "Accuracy:", adaBoost(gameTraining, classify, k+2)['correctRate']

# extra credit