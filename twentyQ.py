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
        self.prevAnswers = {}
        self.timesPlayed = {}
        self.questionsUsed = []
        self.remainingFood = []
        
        data, prevAnswers, times = self.readData()
        
        self.processData(data, prevAnswers, times)
        
    def readData(self):
        # get known data from csv
        data = pd.read_csv('tempData.csv')

        # get sums from csv
        prevAnswers = pd.read_csv('tempWeights.csv')
        
        # get times played
        times = pd.read_csv('timesPlayed.csv')

        # extract questions
        questions = list(data.dtypes.index)
        self.questions = questions[1:]

        #extract data
        data = data.values

        # extract previous answers
        prevAnswers = prevAnswers.values
        
        # extract times played
        times = times.values
        
        return data, prevAnswers, times
    
    def processData(self, data, prevAnswers, times):
        for i in data:
            self.answers[i[0]] = i[1:]
            self.likelihood[i[0]] = 0
            self.remainingFood.append(i[0])
    
        for i in prevAnswers:
            self.prevAnswers[i[0]] = i[1:]
        
        for i in times:
            self.timesPlayed[i[0]] = i[1:]
            
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

        self.questionsUsed.append(self.questions[np.argmin(nextQ)])
        return self.questions[np.argmin(nextQ)]
            
        
    def getNextQuestion(self, currentQ, currentA):
        couldBe = []
        nextQ = []
        possibleQ = []
        countYes = 0
        countNo = 0
        for i in self.answers:
            if self.answers[i][self.questions.index(currentQ)] is currentA:
                couldBe.append(i)
        self.remainingFood = list(set(self.remainingFood) & set(couldBe))
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
                
        choice = random.choice(possibleQ)
        
        self.questionsUsed.append(self.questions[choice])
        return self.questions[choice]
    
    def convertAnswer(self, currentA):
        if currentA is 'yes':
            return 1
        elif currentA is 'no':
            return -1
        else:
            return 0
        
    def updateLikelihood(self, currentQ, currentA):
        for i in self.answers:
            if self.answers[i][self.questions.index(currentQ)] is currentA:
                self.likelihood[i] = self.likelihood[i] + (self.prevAnswers[i][self.questions.index(currentQ)]/self.timesPlayed[i][self.questions.index(currentQ)])
            else:
                self.likelihood[i] = self.likelihood[i] + self.prevAnswers[i][self.questions.index(currentQ)] *-1
                
    def updateWeights(self, answer, correct):
        if correct is True:
            for i in self.questionsUsed:
                self.weightVals[answer][self.questions.index(i)] = self.weightVals[answer][self.questions.index(i)] + (1-self.weightVals[answer][self.questions.index(i)])/2 
                print(self.weightVals[answer][self.questions.index(i)])
        else:
            for i in self.questionsUsed:
                self.weightVals[answer][self.questions.index(i)] = self.weightVals[answer][self.questions.index(i)] - (1-self.weightVals[answer][self.questions.index(i)])/2
                if self.weightVals[answer][self.questions.index(i)] < .0625:
                    self.weightVals[answer][self.questions.index(i)] = .5
                    self.answers[answer][self.questions.index(i)] = -self.answers[answer][self.questions.index(i)]
    
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
