#imports
import numpy as np
from itertools import permutations, combinations
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import math

#constants
EPSILON = 10e-10
NUM = 1000
IMGFILEFORMAT = '.png'
APPROVALPROPORTION = 0.5
MIN_GRAPH = 0.02
OTHER_STRING = "Other"

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
    val = x
    if x > 1:
      val = 1
    elif x < 0:
      val = 0
    stdev = calcSTDEV(val, sample)
    num = np.random.normal(val,stdev)
    while num < 0 or num > 1:
      num = np.random.normal(val,stdev)
    results.append(num)
  results = np.array(results)
  return results

#construct the preference list for RCV iteration
def constructPrefList(partyList, depth):
  return np.asarray(list(permutations(partyList,depth)))

#construct pair list for condorcet iteration
def constructPairList(partyList):
  return np.asarray(list(combinations(partyList,2)))

#figure out the winner of a First past the post election from results
def runFPTP(partyList, results, depth):
  prefList = constructPrefList(partyList, depth)
  partySums = np.zeros(len(partyList))
  for i in range(len(results)):
    index = np.where(partyList == prefList[i][0])[0][0]
    partySums[index] += results[i]
  return np.argmax(partySums)

#figure out the winner of a ranked choice voting election
def runRCV(partyList, results, depth):
  prefList = constructPrefList(partyList, depth)
  pointerList = np.zeros(len(prefList), dtype=int)
  partySums = np.zeros(len(partyList))
  for i in range(len(results)):
    index = np.where(partyList == prefList[i][0])[0][0]
    partySums[index] += results[i]
  while(np.max(partySums) <= (np.sum(partySums)/2)):
    index = np.where(partySums == np.min(partySums[np.nonzero(partySums)]))[0][0]
    for i in range(len(prefList)):
      if (pointerList[i] < len(prefList[i])) and (prefList[i][pointerList[i]] == partyList[index]):
        pointerList[i] += 1
        trying = True
        while(trying):
          if(pointerList[i] < len(prefList[i])):
            newIndex = np.where(partyList == prefList[i][pointerList[i]])[0][0]
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
    index = np.where(partyList == prefList[i][0])[0][0]
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
          partySums[np.where(partyList == prefList[i][pointerList[i]])[0][0]] += results[i]
          trying = False
        else:
          pointerList += 1
          trying = pointerList[i] < len(prefList[i])
      partySums[np.where(partyList == prefList[i][0])[0][0]] -= results[i]
  return np.argmax(partySums)

#figure out winner of an approval election
def runApproval(partyList, results, depth):
  prefList = constructPrefList(partyList, depth)
  partySums = np.zeros(len(partyList))
  if(depth == 1):
    for i in range(len(results)):
      index = np.where(partyList == prefList[i][0])[0][0]
      partySums[index] += results[i]
  else:
    searchDepth = math.min(depth, math.ceil(len(partyList) * APPROVALPROPORTION))
    for i in range(len(results)):
      for j in range(searchDepth):
        index = np.where(partyList == prefList[i][j])[0][0]
        partySums[index] += results[i]
  return np.argmax(partySums)

#figure out winner of a pairwise election (Copeland's method of Condorcet elections)
def runPairwise(partyList, results, depth):
  superiorityList = np.zeros(len(partyList))
  pairList = constructPairList(partyList)
  if(depth == 1):
    for i in range(len(pairList)):
      if results[i] > 0.5:
        index = np.where(partyList == pairList[i][0])[0][0]
        superiorityList[index] += 1
      elif results[i] < 0.5:
        index = np.where(partyList == pairList[i][1])[0][0]
        superiorityList[index] += 1
  else:
    prefList = constructPrefList(partyList, depth)
    for i in range(len(pairList)):
      partyAdvantage = 0
      party1 = pairList[i][0]
      party2 = pairList[i][1]
      for i in range(len(prefList)):
        if (party1 in prefList[i]) and (party2 in prefList[i]):
          indexdif = np.where(prefList[i] == party1)[0][0] - np.where(prefList[i] == party2)[0][0]
          if(indexdif < 0):
            partyAdvantage += results[i]
          else:
            partyAdvantage -= results[i]
        elif(party1 in prefList[i]):
          partyAdvantage += results[i]
        elif(party2 in prefList[i]):
          partyAdvantage -= results[i]
      if partyAdvantage > 0:
        index = np.where(partyList == party1)[0][0]
        superiorityList[index] += 1
      elif partyAdvantage < 0:
        index = np.where(partyList == party2)[0][0]
        superiorityList[index] += 1
  return np.argmax(superiorityList)

#run num iterations of a fptp election
def runFPTPIterations(polling, partyList, num, sample, depth):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    results = normalizePolling(randomizedIteration(normalized, sample))
    winner = runFPTP(partyList, results, depth)
    winList[winner] += 1
  return winList

#run num iterations of a rcv election
def runRCVIterations(polling, partyList, num, sample, depth):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    results = normalizePolling(randomizedIteration(normalized, sample))
    winner = runRCV(partyList, results, depth)
    winList[winner] += 1
  return winList

#run num iterations of a top two election
def runTopTwoIterations(polling, partyList, num, sample, depth):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    results = normalizePolling(randomizedIteration(normalized, sample))
    winner = runTopTwo(partyList, results, depth)
    winList[winner] += 1
  return winList

#run num iterations of an approval election
def runApprovalIterations(polling, partyList, num, sample, depth):
  if(depth == 1):
    normalized = np.array(polling/100)
  else:
    normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    if(depth == 1):
      results = randomizedIteration(normalized, sample)
    else:
      results = normalizePolling(randomizedIteration(normalized, sample))
    winner = runApproval(partyList, results, depth)
    winList[winner] += 1
  return winList

#run num iterations of a pairwise election
def runPairwiseIterations(polling, partyList, num, sample, depth):
  if(depth == 1):
    normalized = np.array(polling/100)
  else:
    normalized = normalizePolling(polling)
  winList = np.zeros(len(partyList))
  for _ in range(num):
    if(depth == 1):
      results = randomizedIteration(normalized, sample)
    else:
      results = normalizePolling(randomizedIteration(normalized, sample))
    winner = runPairwise(partyList, results, depth)
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
        polltype = lines[4*i+4]
        if(polltype[-1] == '\n'):
          polltype = polltype[:-1]
        data.append([np.array(names), np.array(polls), num, polltype])
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
        polltype = lines[lineNum]
        if(polltype[-1] == '\n'):
          polltype = polltype[:-1]
        data.append([np.array(names), polls, num, polltype])
  return data

#print results of election simulation
def printResults(names, results):
  newString = ""
  nameLength = len(max(names, key=len))
  total = np.sum(results)
  for i in range(len(results)):
    s = "{:<" + str(nameLength) + "} {:>6.1%}"
    newString += s.format(names[i],int(results[i])/total) + '\n'
  newString += '\n'
  return newString

#actually run fptp simulation given data from file
def runFPTPElections(npData, num, imgfilepath):
  isPrinting = False
  newString = "FPTP Elections\n\n"
  t = time.process_time()
  for el in npData:
    if(str(el[3]).isnumeric()):
      print("fptp")
      winList = runFPTPIterations(el[1], el[0], num, el[2], int(el[3]))
      newString += printResults(el[0], winList)
      plotResults(el[0], winList, imgfilepath, "Plurality Winner")
      isPrinting = True
  if(isPrinting):
    newString += "Average time: " + str((time.process_time() - t)/len(npData)) + '\n\n'
  else:
    newString = ""
  return newString

#actually run rcv simulation given data from file
def runRCVElections(npData, num, imgfilepath):
  isPrinting = False
  newString = "RCV Elections\n\n"
  t = time.process_time()
  for el in npData:
    if(str(el[3]).isnumeric() and (int(el[3]) > 1)):
      print("rcv")
      winList = runRCVIterations(el[1], el[0], num, el[2], int(el[3]))
      newString += printResults(el[0], winList)
      plotResults(el[0], winList, imgfilepath, "Ranked Choice Winner")
      isPrinting = True
  if(isPrinting):
    newString += "Average time: " + str((time.process_time() - t)/len(npData)) + '\n\n'
  else:
    newString = ""
  return newString

#actually runs a top two runoff simulation given data from file
def runTopTwoElections(npData, num, imgfilepath):
  isPrinting = False
  newString = "Top Two Elections\n\n"
  t = time.process_time()
  for el in npData:
    if(str(el[3]).isnumeric() and (int(el[3]) > 1)):
      print("top2")
      winList = runTopTwoIterations(el[1], el[0], num, el[2], int(el[3]))
      newString += printResults(el[0], winList)
      plotResults(el[0], winList, imgfilepath, "Top Two Winner")
      isPrinting = True
  if(isPrinting):
    newString += "Average time: " + str((time.process_time() - t)/len(npData)) + '\n\n'
  else:
    newString = ""
  return newString

#actually runs an approval simulation given data from file
def runApprovalElections(npData, num, imgfilepath):
  isPrinting = False
  newString = "Approval Elections\n\n"
  t = time.process_time()
  for el in npData:
    isBigNumber = str(el[3]).isnumeric() and int(el[3]) > 1
    isPairwise = el[3] == 'a'
    if(isBigNumber or isPairwise):
      print("app")
      depthNum = 1
      if(isBigNumber):
        depthNum = int(el[3])
      winList = runApprovalIterations(el[1], el[0], num, el[2], depthNum)
      newString += printResults(el[0], winList)
      plotResults(el[0], winList, imgfilepath, "Approval Winner")
      isPrinting = True
  if(isPrinting):
    newString += "Average time: " + str((time.process_time() - t)/len(npData)) + '\n\n'
  else:
    newString = ""
  return newString

#actually runs a pairwise simulation given data from file
def runPairwiseElections(npData, num, imgfilepath):
  isPrinting = False
  newString = "Pairwise Elections\n\n"
  t = time.process_time()
  for el in npData:
    isBigNumber = str(el[3]).isnumeric() and int(el[3]) > 1
    isPairwise = el[3] == 'p'
    if(isBigNumber or isPairwise):
      print("pair")
      depthNum = 1
      if(isBigNumber):
        depthNum = int(el[3])
      winList = runPairwiseIterations(el[1], el[0], num, el[2], depthNum)
      newString += printResults(el[0], winList)
      plotResults(el[0], winList, imgfilepath, "Pairwise Winner")
      isPrinting = True
  if(isPrinting):
    newString += "Average time: " + str((time.process_time() - t)/len(npData)) + '\n\n'
  else:
    newString = ""
  return newString

#runs all the electoral systems for a particular file
def doAllSystems(name, filepath, imgfilepath, num, nested):
  newString = name + '\n'
  if(not nested):
    data = readFromFile(filepath)
  else:
    data = readFromFileNested(filepath)
  newString += runFPTPElections(data, num, imgfilepath)
  newString += runRCVElections(data, num, imgfilepath)
  newString += runTopTwoElections(data, num, imgfilepath)
  newString += runApprovalElections(data, num, imgfilepath)
  newString += runPairwiseElections(data, num, imgfilepath)
  return newString

#process a text file in order to send its data to the client
def processData(filepath, fileroot):
  data = readFromFile(filepath)
  candString = ""
  for el in data[0][0]:
    candString += str(el) + ', '
  candString = candString[:-2]
  pollString = ""
  for el in data[0][1]:
    pollString += str(el) + ', '
  pollString = pollString[:-2]
  obj = {
    "candString": candString,
    "pollString": pollString,
    "sample_size": str(data[0][2]),
    "filename_root": fileroot
  }
  return obj

#plot results
def plotResults(partyList, resultList, imgfilepath, title):
  newDict = {}
  for i in range(len(partyList)):
    if(resultList[i] >= (MIN_GRAPH * NUM)):
      newDict[partyList[i]] = resultList[i]
    elif(resultList[i] > 0):
      if OTHER_STRING not in newDict:
        newDict[OTHER_STRING] = 0
      newDict[OTHER_STRING] += resultList[i]
  plt.pie(newDict.values(), labels=newDict.keys(), autopct='%1.1f%%')
  plt.axis('equal')
  plt.tight_layout()
  plt.title(title)
  numstr = str(len(glob(imgfilepath+ '*')))
  plt.savefig(imgfilepath + numstr + IMGFILEFORMAT, bbox_inches='tight')
  plt.clf()