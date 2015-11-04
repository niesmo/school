import json
import random
import sys
from numpy import *

from lib import *
from k_means import *


N = DEFAULT_N = 10;
printPlot = False;
dim = DEFAULT_DIM = 2;
trainingFilename = "training.json";
testingFilename = "testing.json";

for i in range(len(sys.argv)):
  temp = sys.argv[i];

  # finding the k for k-means
  ind = temp.upper().find('-N=')
  if not ind == -1:
    N = int(temp[3:]);
    continue;
  # finding to whether plot or not   
  ind = temp.upper().find('-PLOT=')
  if not ind == -1:
    printPlot = True if temp[6:] == 'TRUE' else False;
    continue;

  # finding the dimentionality of the data
  ind = temp.upper().find('-D=')
  if not ind == -1:
    dim = int(temp[3:])
    continue;

  ind = temp.upper().find('-TRAINING=')
  if not ind == -1:

    trainingFilename = str(temp[10:])
    continue;
  
  ind = temp.upper().find('-TESTING=')
  if not ind == -1:
    testingFilename = str(temp[10:])
    continue;


'''
Reading the training data
'''
f=open(trainingFilename,'r')
trainingdata=json.load(f)
traininglabels=array(trainingdata['labels'])
trainingpoints=array(trainingdata['points'])
f.close()




# get the vectors usign k-means
vectors = k_means(trainingpoints, N, True);

'''
***************************** PART 1 *****************************
'''

# preparing the data for matplot
if printPlot:
  import matplotlib.pyplot as plt
  
  x = [];
  y = [];

  for point in trainingpoints:
    x.append(point[0]);
    y.append(point[1]);

  # plot the points
  plt.scatter(x,y, marker='.');

  x = [];
  y = [];
  for v in vectors:
    x.append(v[0]);
    y.append(v[1]);

  plt.scatter(x,y, c='r', marker="o", s=100);


  # plotting the the points
  plt.show();


'''
***************************** PARTS 2,3 *****************************
'''
probabilities = getProbabilities(trainingpoints, traininglabels, vectors, True);



'''
***************************** PART 3 *****************************
'''

#Reading the testing data
f=open('testing.json','r')
trainingdata=json.load(f)
testinglabels=array(trainingdata['labels'])
testingpoints=array(trainingdata['points'])
f.close()


# errorCounts = [];
errorRates = [];
for i in range(10):
  # run k-means
  vectors = k_means(trainingpoints, N, False);

  # get the probabilities
  probabilities = getProbabilities(trainingpoints, traininglabels, vectors, False);
  
  # get the error when classifing the test data 
  errorCount = classify(testingpoints, testinglabels, vectors, probabilities['labelGivenVectorProbability']);

  # adding the error count to an array
  # errorCounts.append(errorCount);
  errorRates.append(errorCount/float(len(testingpoints)));

# print "Average error count: ", mean(errorCounts);
print "\n\n{0:<25} {1:<10}".format("Average error rate:", round(mean(errorRates),5));
# print "STD error count: ", std(errorCounts)
print "{0:<25} {1:<10}".format("STD error rate:", round(std(errorRates),5));
print

'''
***************************** PART 4 *****************************
Sample the average/standard deviation of the classification error rate for k=2,5,6,8,12,15,20,50
'''
k_values = [2,5,6,8,12,15,20,50]
averageErrors = [];
errorStds = [];

for k in k_values:
  # errorCounts = [];
  errorRates = [];
  for i in range(10):
    # run k-means
    vectors = k_means(trainingpoints, k, False);

    # get the probabilities
    probabilities = getProbabilities(trainingpoints, traininglabels, vectors, False);
    
    # get the error when classifing the test data 
    errorCount = classify(testingpoints, testinglabels, vectors, probabilities['labelGivenVectorProbability']);

    # adding the error count to an array
    # errorCounts.append(errorCount);
    errorRates.append(errorCount/float(len(testingpoints)));

  averageErrors.append(mean(errorRates));
  errorStds.append(std(errorRates));

  print "For k = {0:<3} AVG: {1:<10} STD: {2:<10}".format(k, round(mean(errorRates),4), round(std(errorRates),4))
  # print "For k = ", k, "AVG: ", mean(errorRates), "STD: ", std(errorRates)

print "\nThe overal error rate AVG: ", mean(averageErrors);
print "The overal error rate STD: ", std(errorStds);