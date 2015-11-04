# Returns the index of the nearest vector to the given point
# Points are given in array [x,y]
def findNearestVector(p,vectors):
  index = 0;
  i=0;
  minD = 1000;
  for v in vectors:
    tempD = dist(p,v)
    if tempD < minD:
      minD = tempD;
      index = i;

    i+=1
  return index;

# Distant between two points
# points are given as arrays [x,y]
def dist(a, b, D=2):
  cSquared = 0;
  for i in range(D):
    cSquared += (b[i] - a[i])**2;

  return cSquared**0.5;  
  # return ((b[1] - a[1])**2 + (b[0] - a[0])**2)**0.5;

def makeTableFormat(N):
  tableFormat = "";
  for i in range(N):
    tableFormat += "| {"+str(i)+":<10} ";
  return tableFormat + '|';

# this function will calculate all the probabilities and will return them in an object
# Probabilities: 
#   label
#   vector
#   vector given label
#   label given vector
def getProbabilities(points, labels, vectors, printable):
  N = len(vectors);
  '''
  ***************************** PART 2 *****************************
  calculate P(V|C) and P(C) and P(C|V)
  Where C is the label from the training data
  '''
  # calculate the frequency of the lables
  pointCount = 0
  labelFrequency = {};
  for label in labels:
    pointCount += 1;
    if labelFrequency.has_key(label):
      labelFrequency[label] += 1;
    else:
      labelFrequency[label] = 1;

  # normalizing the frequencies
  labelProbability = {};
  for lf in labelFrequency:
    labelProbability[lf] = labelFrequency[lf]/float(pointCount);

  vectorGivenLabelCount = {};

  # calculating the P(V|C)
  for lf in labelFrequency:
    if not vectorGivenLabelCount.has_key(lf):
      vectorGivenLabelCount[lf] = [0]*N;
    
  # calculating the count
  for i, point in enumerate(points):
    nearestVectorIndex = findNearestVector(point, vectors);
    vectorGivenLabelCount[labels[i]][nearestVectorIndex]+=1

  # calculating the actual probability
  vectorGivenLabelProbability = {};
  for c in vectorGivenLabelCount:
    vectorGivenLabelProbability[c] = []
    for i,v in enumerate(vectorGivenLabelCount[c]):
      vectorGivenLabelProbability[c].append(round(vectorGivenLabelCount[c][i]/float(labelFrequency[c]),5));

  if printable:
    # Printing the P(V|C) table
    print "\n\n*********** P(V|C) TABLE ***********"
    tableFormat = makeTableFormat(N+1);
    # tableFormat = "| {:<10} " * (N+1) + '|';
    headers = ['C'];
    for i in range(len(vectors)):
      headers.append('V' + str(i+1));

    hr = '-'*((13*(N+1))+1);
    print hr;
    print tableFormat.format(*headers);
    print hr;
    for c in vectorGivenLabelProbability:
      print tableFormat.format(c, *vectorGivenLabelProbability[c]);
    print hr;

  if printable:
    # Print the P(C) table
    print "\n\n*********** P(C) TABLE ***********"
    tableFormat = makeTableFormat(2);
    # tableFormat = "|{:<10} | {:<10}|"
    hr = '-'*(20+7);
    print hr;
    print tableFormat.format("C", "P(C)");
    print hr;
    
    for p in labelProbability:
      print tableFormat.format(p, labelProbability[p]);
    print hr;

  '''
  ***************************** PART 3 *****************************
  Calculate P(C|V) = aP(V|C)*P(C) = (P(V|C)*P(C))/P(V)
           P(V|C)*P(C)
  P(C|V) = -----------
              P(V)
  '''
  # calculate p(v)
  vectorProbability = {};

  for i, v in enumerate(vectors):
    vectorProbability[i] = v[4]/float(pointCount);

  if printable:
    # Print the P(V) table
    print "\n\n*********** P(V) TABLE ***********"
    tableFormat = makeTableFormat(2);
    # tableFormat = "|{:<10} | {:<10}|"
    hr = '-'*(20+7);
    print hr;
    print tableFormat.format("V", "P(V)");
    print hr;
    for p in vectorProbability:
      print tableFormat.format(p, vectorProbability[p]);
    print hr;

  labelGivenVectorProbability = {};
  for i, v in enumerate(vectors):
    pvc = [];
    for c in labelProbability:
      if not labelGivenVectorProbability.has_key(i):
        labelGivenVectorProbability[i] = [];

      # getting rid of rounding problem (or is something fundamentally wrong :) )
      temp = round(vectorGivenLabelProbability[c][i] * labelProbability[c] / vectorProbability[i],6)
      temp = 1. if temp > 1 else temp;

      labelGivenVectorProbability[i].append(temp);
      # pvc.append(vectorGivenLabelProbability[c][i]);

  if printable:
    # printing the P(C|V) table
    print "\n\n*********** P(C|V) TABLE ***********"
    # tableFormat = "| {:<10} " * (len(labelProbability) + 1) + "|";
    tableFormat = makeTableFormat(len(labelProbability) + 1);
    headers = ['V'];
    for c in labelProbability:
      headers.append('C' + str(c))

    hr = '-'*((13*(len(labelProbability)+1))+1);

    print hr
    print tableFormat.format(*headers)
    print hr
    for v in labelGivenVectorProbability:
      print tableFormat.format(v, *labelGivenVectorProbability[v]);
    print hr;

  # setting up the object to return
  probabilities = {};
  
  probabilities['labelProbability'] = labelProbability;
  probabilities['vectorProbability'] = vectorProbability;
  probabilities['vectorGivenLabelProbability'] = vectorGivenLabelProbability;
  probabilities['labelGivenVectorProbability'] = labelGivenVectorProbability;

  return probabilities

def mean(l):
  return sum(l)/float(len(l));

def classify(points, labels, vectors, labelGivenVectorProbability):
  errorCount = 0;
  for i, point in enumerate(points):
    nearestVectorIndex = findNearestVector(point, vectors)
    labelGuess = labelGivenVectorProbability[nearestVectorIndex].index(max(labelGivenVectorProbability[nearestVectorIndex]))

    # print 'Guess: ', labelGuess, 'Actual: ', testinglabels[i]
    if not labelGuess == labels[i]:
      errorCount += 1;

  return errorCount;