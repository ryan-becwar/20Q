import numpy as np
import pandas as pd
import csv
import copy as cp
import random

class twentyQ(object):
    def __init__(self):
        self.questions = []
        self.answers = {}
        self.likelihood = {}
        self.weightVals = {}
        self.questionsUsed = []
        self.remainingFood = []
        
        data, weights = self.readData()
        
        self.processData(data, weights)
        
    def readData(self):
        # get known data from csv
        data = pd.read_csv('tempData.csv')

        # get weights from csv
        weights = pd.read_csv('tempWeights.csv')

        # extract questions
        questions = list(data.dtypes.index)
        self.questions = questions[1:]

        #extract data
        data = data.values

        # extract weights
        weights = weights.values
        
        return data, weights
    
    def processData(self, data, weights):
        for i in data:
            self.answers[i[0]] = i[1:]
            self.likelihood[i[0]] = 0
            self.remainingFood.append(i[0])
    
        for i in weights:
            self.weightVals[i[0]] = i[1:]
            
    def getFirstQuestion(self):
        countYes = 0
        countNo = 0
        nextQ = []
        possibleQ = []
        for j in range(0,len(self.questions)):
            for i in self.answers:
                if self.answers[i][j] == 1:
                    countYes = countYes + 1
                elif self.answers[i][j] == -1:
                    countNo = countNo + 1
            nextQ.append(abs(countYes - countNo))
            countYes = countNo = 0
            
        for i in range(len(nextQ)):
            if nextQ[i] == np.min(nextQ):
                possibleQ.append(i)
                
        choice = random.choice(possibleQ)

        self.questionsUsed.append(np.argmin(nextQ))
        return self.questions[np.argmin(nextQ)]
            
    def answerQuestion(self, currentQ, currentA):
        self.updateLikelihood(currentQ, currentA)

        couldBe = []
        for i in self.answers:
            if self.answers[i][currentQ] is currentA:
                couldBe.append(i)
        self.remainingFood = list(set(self.remainingFood) & set(couldBe))

        
    def getNextQuestion(self):
        nextQ = []
        possibleQ = []
        countYes = 0
        countNo = 0
        for j in range(0,len(self.questions)):
            for i in self.remainingFood:
                if self.answers[i][j] == 1:
                    countYes = countYes + 1
                elif self.answers[i][j] == -1:
                    countNo = countNo + 1
            nextQ.append(abs(countYes - countNo))
            countYes = countNo = 0
            
        for i in range(len(nextQ)):
            if nextQ[i] == np.min(nextQ):
                possibleQ.append(i)
                
        remainingPossible = list(set(possibleQ) - set(self.questionsUsed))
        if remainingPossible:
            choice = random.choice(remainingPossible)
            self.questionsUsed.append(choice)
            return self.questions[choice]
        else:
            return None
    
    def convertAnswer(self, currentA):
        if currentA is 'yes' or currentA is 'y':
            return 1
        elif currentA is 'no' or currentA is 'n':
            return -1
        else:
            return 0
        
    def updateLikelihood(self, currentQ, currentA):
        for i in self.answers:
            if self.answers[i][currentQ] is currentA:
                self.likelihood[i] = self.likelihood[i] + self.weightVals[i][currentQ] *1
            else:
                self.likelihood[i] = self.likelihood[i] + self.weightVals[i][currentQ] *-1
                
    def updateWeights(self, answer, correct):
        if correct is True:
            for i in self.questionsUsed:
                self.weightVals[answer][i] = self.weightVals[answer][i] + (1-self.weightVals[answer][i])/2 
                print(self.weightVals[answer][i])
        else:
            for i in self.questionsUsed:
                self.weightVals[answer][i] = self.weightVals[answer][i] - (1-self.weightVals[answer][i])/2
                if self.weightVals[answer][i] < .0625:
                    self.weightVals[answer][i] = .5
                    self.answers[answer][i] = -self.answers[answer][i]
    
    def writeToCSV(self):
        Qs = cp.deepcopy(self.questions)
        Qs.insert(0, ' ')
        
        #copy data to csv
        myfile = open('tempData.csv', 'w')
        with myfile:
            myFields = Qs
            writer = csv.DictWriter(myfile, fieldnames=myFields)    
            writer.writeheader()
            for i in self.answers:
                newlist = [i]
                for j in self.answers[i]:
                    newlist.append(j)
                writer.writerow({Qs[k]:newlist[k] for k in range(len(Qs))})
                    
        # copy weights to csv
        myfile = open('tempWeights.csv', 'w')
        with myfile:
            myFields = Qs
            writer = csv.DictWriter(myfile, fieldnames=myFields)    
            writer.writeheader()
            for i in self.weightVals:
                newlist = [i]
                for j in self.weightVals[i]:
                    newlist.append(j)
                writer.writerow({Qs[k]:newlist[k] for k in range(len(Qs))})
