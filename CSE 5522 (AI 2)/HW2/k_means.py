import random
import sys
from lib import *

#CONSTANTS
MIN_X = -25;
MAX_X = 25;
MIN_Y = -25;
MAX_Y = 25;

def generateRandomVector(dim):
  vec = [];
  # generate the points
  for i in range(dim):
    vec.append(random.uniform(MIN_X, MAX_X))
    
  return vec;

  # x = random.uniform(MIN_X, MAX_X);
  # y = random.uniform(MIN_Y, MAX_Y);
  # return [x,y];

def assignPointToVector(point, vector, dim):
  if len(vector) == dim:
    # if the vector has size 2, this is the first time a point is being assigned to it
    # the 3rd and 4th spot in the vector is for the average of the points assigned to the vector
    for i in range(dim):
      vector.append(point[i]);
    
    vector.append(1);

  else:
    # take average of the current average and the nearest point to this vector
    for i in range(dim):
      vector[dim+i] = (vector[dim+1] + point[i])/2;

    vector[dim] += 1;
    # vector[2] = (vector[2] + point[0])/2;
    # vector[3] = (vector[3] + point[1])/2;
    # vector[4] += 1

def findAverageChangeForVectors(averageChange, vectors, dim):
  for v in vectors:
    if(len(v) > 2):
      p1 = [v[0], v[1]]
      p2 = [v[2], v[3]]
      if averageChange == 100:
        averageChange = dist(p1,p2)
      else:
        averageChange = (averageChange + dist(p1,p2))/2;

  return averageChange;

def updateVectors(vectors, dim):
  for v in vectors:
    if(len(v) > 2):
      v[0] = v[2];
      v[1] = v[3];

def updateVectorsWithNoPointsAssigned(vectors, dim):
  vLeft = False;
  for i, v in enumerate(vectors):
    if len(v) == 2 or v[4] == 0:
      vectors[i] = generateRandomVector();
      vLeft = True;
  return vLeft;

def resetPointCountsAssignedToVectors(vectors, dim):
  for v in vectors:
    if len(v) == 5:
      v[4] = 0

def k_means(points, k, printable):
  # VARIABLES
  dim = len(points[0]);
  epsilon = 0.000000001; # it works with absolute zero too :)
  iterationCount = 0;
  averageChange = 100;
  vectors = [];
  vectorWithNoPointsAssigned = True;

  # INITIALIZATION 
  # create N vectors with random points in them
  for i in range(k):
    vectors.append(generateRandomVector());


  # averageChange[0] > epsilon or averageChange[1] > epsilon
  while(vectorWithNoPointsAssigned or averageChange > epsilon):
    # reset the point counts that are assigned to vectors so its not double counting
    resetPointCountsAssignedToVectors(vectors);

    # Incrementing the increment count
    iterationCount+=1;

    # for every point 
    for point in points:

      # find the nearest vector to the point
      nearestVectorIndex = findNearestVector(point, vectors)

      # assign that point the nearest vector
      assignPointToVector(point, vectors[nearestVectorIndex], dim);

    # find the average change in the vectors 
    averageChange = findAverageChangeForVectors(averageChange, vectors, dim)

    # update the vectors to the average of the points assigned to this vector
    updateVectors(vectors);

    # check if there is any vector that has no point assigned to it
    vectorWithNoPointsAssigned = updateVectorsWithNoPointsAssigned(vectors);

  # Statistics for the iteration count
  if printable:
    print "It took", iterationCount, "iterations to find the solution"

  return vectors