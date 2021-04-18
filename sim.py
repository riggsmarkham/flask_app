#imports
import numpy as np
from itertools import permutations
import time

#constants
EPSILON = 10e-10
NUM = 1000

#normalize polling to decimals between 0 (none) and 1 (all)
def normalizePolling(polling):
  return np.array(polling/np.sum(polling))

#calculate standard deviation for a sample proportion
def calcSTDEV(x, sample):
  return np.sqrt(((1-x)*x)/sample)

#generate randomized iteration of polling
def randomizedIteration(polling, sample):
  results = []
  for x in polling:
    stdev = calcSTDEV(x, sample)
    num = np.random.normal(x,stdev)
    while num < 0 or num > 1:
      num = np.random.normal(x,stdev)
    results.append(num)
  results = np.array(results)
  return np.array(results/np.sum(results))

#construct the preference list for RCV iteration
def constructPrefList(partyList, depth):
  return np.asarray(list(permutations(partyList,depth)))

#figure out the winner of a First past the post election from results
def runFPTP(partyList, results, depth):
  prefList = constructPrefList(partyList, depth)
  partySums = np.zeros(len(partyList))
  for i in range(len(results)):
    index = np.where(partyList == prefList[i][0])
    partySums[index] += results[i]
  return np.argmax(partySums)

#figure out the winner of a ranked choice voting election
def runRCV(partyList, results, depth):
  prefList = constructPrefList(partyList, depth)
  pointerList = np.zeros(len(prefList), dtype=int)
  partySums = np.zeros(len(partyList))
  for i in range(len(results)):
    index = np.where(partyList == prefList[i][0])
    partySums[index] += results[i]
  while(np.max(partySums) <= (np.sum(partySums)/2)):
    index = np.where(partySums == np.min(partySums[np.nonzero(partySums)]))
    for i in range(len(prefList)):
      if (pointerList[i] < len(prefList[i])) and (prefList[i][pointerList[i]] == partyList[index]):
        pointerList[i] += 1
        trying = True
        while(trying):
          if(pointerList[i] < len(prefList[i])):
            newIndex = np.where(partyList == prefList[i][pointerList[i]])
            if(partySums[newIndex] != 0):
              partySums[newIndex] += results[i]
              trying = False
            else:
              pointerList[i] += 1
          else:
            trying = False
        partySums[index] -= results[i]
    if(np.absolute(partySums[index]) <= EPSILON):
      partySums[index] = 0
    else:
      raise ValueError("didn't reduce to zero")
  return np.argmax(partySums)

#figure out winner of a top two election
def runTopTwo(partyList, results, depth):
  prefList = constructPrefList(partyList, depth)
  pointerList = np.zeros(len(prefList), dtype=int)
  partySums = np.zeros(len(partyList))
  for i in range(len(results)):
    index = np.where(partyList == prefList[i][0])
    partySums[index] += results[i]
  temp = np.argpartition(-partySums, 2)
  result_args = temp[:2]
  topParties = [partyList[result_args[0
  ]],partyList[result_args[1]]]
  for i in range(len(prefList)):
    if(prefList[i][0] not in topParties):
      pointerList[i] += 1
      trying = pointerList[i] < len(prefList[i])
      while(trying):
        if(prefList[i][pointerList[i]] in topParties):
          partySums[np.where(partyList == prefList[i][pointerList[i]])] += results[i]
          trying = False
        else:
          pointerList += 1
          trying = pointerList[i] < len(prefList[i])
      partySums[np.where(partyList == prefList[i][0])] -= results[i]
  return np.argmax(partySums)

#run num iterations of a fptp election
def runFPTPIterations(polling, partyList, num, sample, depth):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    results = randomizedIteration(normalized, sample)
    winner = runFPTP(partyList, results, depth)
    winList[winner] += 1
  return winList

#run num iterations of a rcv election
def runRCVIterations(polling, partyList, num, sample, depth):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    results = randomizedIteration(normalized, sample)
    winner = runRCV(partyList, results, depth)
    winList[winner] += 1
  return winList

#run num iterations of a top two election
def runTopTwoIterations(polling, partyList, num, sample, depth):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    results = randomizedIteration(normalized, sample)
    winner = runTopTwo(partyList, results, depth)
    winList[winner] += 1
  return winList

#read data from a file
def readFromFile(filename):
  data = []
  with open(filename) as infile:
      lines = infile.readlines()
      n = int(lines[0][0])
      for i in range(n):
        names = lines[4*i+1].split(',')
        names[-1] = names[-1][:-1]
        polls = list(map(int,lines[4*i+2][:-1].split(',')))
        if(np.any(np.less(polls,0))):
          raise ValueError("negative input poll")
        num = int(lines[4*i+3])
        depth = int(lines[4*i+4])
        data.append([np.array(names), np.array(polls), num, depth])
  return data

#read a file with 2nd choice picks
def readFromFileNested(filename):
  data = []
  with open(filename) as infile:
      lines = infile.readlines()
      n = int(lines[0][0])
      lineNum = 0
      for _ in range(n):
        lineNum += 1
        names = lines[lineNum].split(',')
        names[-1] = names[-1][:-1]
        firstPolls = np.array(list(map(int,lines[lineNum + 1][:-1].split(','))))
        if(np.any(np.less(firstPolls,0))):
          raise ValueError("negative input poll")
        polls = np.empty(len(firstPolls)*(len(firstPolls)-1))
        for j in range(len(firstPolls)):
          secondPolls = np.array(list(map(int,lines[lineNum + 2 + j][:-1].split(','))))
          if(np.any(np.less(secondPolls,0))):
            raise ValueError("negative input poll")
          normalized = normalizePolling(secondPolls)
          polls[len(normalized)*j:len(normalized)*(j+1)] = normalized * firstPolls[j]
        lineNum += 3 + len(firstPolls)
        num = int(lines[lineNum - 1])
        depth = int(lines[lineNum])
        data.append([np.array(names), polls, num, depth])
  return data

#print results of election simulation
def printResults(names, results):
  nameLength = len(max(names, key=len))
  total = np.sum(results)
  for i in range(len(results)):
    s = "{:<" + str(nameLength) + "} {:>6.1%}"
    print(s.format(names[i],int(results[i])/total))
  print()

#actually run fptp simulation given data from file
def runFPTPElections(npData, num):
  print("FPTP Elections\n")
  t = time.process_time()
  for el in npData:
    printResults(el[0], runFPTPIterations(el[1], el[0], num, el[2], el[3]))
  print("Average time: " + str((time.process_time() - t)/len(npData)))
  print()

#actually run rcv simulation given data from file
def runRCVElections(npData, num):
  print("RCV Elections\n")
  t = time.process_time()
  for el in npData:
    printResults(el[0], runRCVIterations(el[1], el[0], num, el[2], el[3]))
  print("Average time: " + str((time.process_time() - t)/len(npData)))
  print()

#actually runs a top two runoff simulation given data from file
def runTopTwoElections(npData, num):
  print("Top Two Elections\n")
  t = time.process_time()
  for el in npData:
    printResults(el[0], runTopTwoIterations(el[1], el[0], num, el[2], el[3]))
  print("Average time: " + str((time.process_time() - t)/len(npData)))
  print()

#runs all the electoral systems for a particular file
def doAllSystems(name, filename, num, nested):
  print(name)
  if(not nested):
    data = readFromFile(filename)
  else:
    data = readFromFileNested(filename)
  runFPTPElections(data, num)
  runRCVElections(data, num)
  runTopTwoElections(data, num)

#process a text file in order to send its data to the client
def processData(filename):
  return

# doAllSystems('Quick Color Parties', 'data/simplecolors.txt', NUM, False)
# doAllSystems('NYC Mayor', 'data/nycmayor.txt', NUM, False)
# doAllSystems('Big Color Parties','data/rankedcolors.txt', NUM, False)
# doAllSystems('Canada?', 'data/canada.txt', NUM, True)