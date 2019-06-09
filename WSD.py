from math import log2
from string import punctuation
import re
import copy
import sys


def getInstanceCount(text):
   # for line in inputData.split('\n'): #get data between head tags
    return len(re.findall(r'<head>\S+</head>',text))

def getInstanceData(allText):
   # for line in inputData.split('\n'): #get data between head tags
   answer = dict()
   senseDict = dict()
   instanceDict = dict()
   for para in allText.split("\n\n"):
        innerText = getInnerData('<instance id=\"','</instance>', para)
        if innerText=="":
            continue
        
        index  = innerText.index('\" docsrc')
        instanceId = innerText[:index]
        if not instanceId in instanceDict:
            instanceDict[instanceId] = list()
        answerContent =  getInnerData('<answer','/>', innerText)
        senseId = getInnerData('senseid=\"','\"',answerContent)
        answer[instanceId] = senseId
        if senseId not in senseDict:
            senseDict[senseId] = list()
        contentData = getInnerData("<context>", "</context>", innerText)
        for data in contentData.split(" "):
            data = data.strip('\n')
            data = data.lower()
            data = strip_stopwords(data)
            if data != "":
                senseDict[senseId].append(data)
                instanceDict[instanceId].append(data)
   return (answer,senseDict,instanceDict) 

def makeTestTrainData(instanceDict):
    test = dict()
    train = dict()
    instancePerFold = int(len(instanceDict)/5) +1
    #print(instancePerFold)
    for i in range(0,5):
        test[i] = dict()
        train[i] = dict()
        test[i] = dict()
    f =0
    p=0
    for instanceId in instanceDict:
        test[f][instanceId] = instanceDict[instanceId].copy()
        p +=1
        if(p==instancePerFold):
            f+=1
            p=0
    for i in range(0,5):
        for j in range(0,5):
            if(i!=j):
               train[i].update(test[j]) 

    return test,train

def getInnerData(start, end, text):
	innerText = ""
	if text.find(start)!=-1:
		startword = text[text.find(start):text.rfind(end)]
		innerText = startword[len(start):]
	return innerText
     


def strip_stopwords(data):
	return ''.join(content for content in data if content not in punctuation)    

def wsd(inputFile,outputFile):
    inputData = inputFile.read()
    #print(plant)
    inputFile.close() 
    
    
    answer,senseDict,instanceDict = getInstanceData(inputData)
    totalsenses = 0 
    senseprobdict = dict()
    for sense in senseDict:
        totalsenses += len(senseDict[sense])
    for sense in senseDict:
        senseprobdict[sense] = len(senseDict[sense] )/ totalsenses #calculate sense probabilities
    
    senseDictUnique = dict()
    senseDictUniquenum = dict()
    for sense in senseDict:
        senseDictUnique[sense] = list()
        senseDictUniquenum[sense] = 0
        for data in senseDict[sense]:
            if not data in senseDictUnique[sense]:
                senseDictUnique[sense].append(data)
            senseDictUniquenum[sense] = len(senseDictUnique[sense]) #get unique content per sense

    
    test, train = makeTestTrainData(instanceDict)

  #  probDict = dict()
    probWordDict = dict()
    finaldict = dict()
    totalaccuracy =0.00
    for i in range(0,5):
        #probDict[i] = dict()
        probWordDict[i] = dict()
        finaldict[i] = dict()
        for instanceId in train[i].keys():
            for sense in senseDict:
                totalprob = 0
                for data in train[i][instanceId]:
                    if  data not in probWordDict[i]:
                        probWordDict[i][data] = dict()
                    if  sense not in probWordDict[i][data]:
                        probWordDict[i][data][sense] = 0
                    value1 = senseDict[sense].count(data) + 1 
                    value2 = len(senseDict[sense]) + senseDictUniquenum[sense]
                    prob = log2(value1/value2)

                    probWordDict[i][data][sense]  += prob 
                    totalprob +=prob
                #sensetotalprob = log2(senseprobdict[sense])+totalprob
                
                #probDict[i][instanceid].append({sense:sensetotalprob})

        '''for instanceid in probDict[i]:
            value1 = -sys.float_info.max
            for finalList in probDict[i][instanceid]:
                for sense in finalList:
                    value = finalList[sense]
                    if(value > value1):
                        finalsense = sense
                        value1 = value
            finaldict[i][instanceid] = finalsense'''
        
        for instanceId in test[i].keys():
            probSenses = dict()
            n=0
            
            for data in instanceDict[instanceId]:
            
                if data in probWordDict[i]:
                    n +=1
                    for sense in probWordDict[i][data].keys():
                        if sense not in probSenses:
                            probSenses[sense] =0
                        probSenses[sense] +=probWordDict[i][data][sense] 
            #print(str(len(probSenses)))
            #print(str(n))
            maxValue = -sys.float_info.max
            finalsense =''
            for sense in probSenses:
                if probSenses[sense]>maxValue:
                    maxValue = probSenses[sense]  + log2(senseprobdict[sense])
                    finalsense = sense
            finaldict[i][instanceId] = finalsense
            #print(instanceId+ ' '+finalsense + ' '+ answer[instanceId] + ' '+ str(maxValue))

        correct = 0
        total = 0
        for key in finaldict[i]:
            if key in answer:
                total += 1
                if answer[key] == finaldict[i][key]:
                    correct += 1
        accuracy = (correct/total)*100    
        print("Accuracy fold" +str(i+1)+" =",(correct/total)*100)
        totalaccuracy +=accuracy
    totalaccuracy = totalaccuracy/5
    print("Total Accuracy =",totalaccuracy)
    for i in range(0,5):
        outputFile.write("Fold"+str(i+1)+"\n\r")
        for key in finaldict[i]:
            outputFile.write(key+ ' '+finaldict[i][key]+'\n\r')

def main():
    inputFileString = sys.argv[1]
    inputFile = open(inputFileString)
    outputFileString  =inputFileString +'.out'

    
    outputFile = open(outputFileString,'w')
    
    wsd(inputFile,outputFile)
    
        
if __name__ == "__main__":
    main()     