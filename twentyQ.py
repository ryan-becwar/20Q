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
        self.answersGiven = []
        
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
                elif self.answers[i][j] == 0:
                    countNo = countNo + 1
            nextQ.append(abs(countYes - countNo))
            countYes = countNo = 0
            
        for i in range(0,len(nextQ)):
            if nextQ[i] == np.min(nextQ):
                possibleQ.append(i)
        choice = random.choice(possibleQ)

        self.questionsUsed.append(choice)
        return self.questions[choice]
            
        
    def getNextQuestion(self):
        nextQ = []
        possibleQ = []
        countYes = 0
        countNo = 0
        for j in range(0,len(self.questions)):
            for i in self.remainingFood:
                if self.answers[i][j] == 1:
                    countYes = countYes + 1
                elif self.answers[i][j] == 0:
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
    
    def answerQuestion(self, currentQ, currentA):
        self.updateLikelihood(currentQ, currentA)

        couldBe = []
        for i in self.answers:
            if self.answers[i][currentQ] is currentA:
                couldBe.append(i)
        self.remainingFood = list(set(self.remainingFood) & set(couldBe))

    def convertAnswer(self, currentA):
        if currentA == 'yes' or currentA == 'y':
            return 1
        elif currentA == 'no' or currentA == 'n':
            return 0
        else:
            return -1
        
    def updateLikelihood(self, currentQ, currentA):
        #append the answer
        self.answersGiven.append(currentA)
        
        # update the likelihood
        for ans in self.answers:
            if self.answers[ans][currentQ] is currentA:
                #if the answer is no then add the average number of 'nos' for that question
                if currentA is 0:
                    self.likelihood[ans] = self.likelihood[ans] + (1-self.prevAnswers[ans][currentQ])
                #otherwise do the average number of yeses.  
                else:
                    self.likelihood[ans] = self.likelihood[ans] + (self.prevAnswers[ans][currentQ])
                    
    def getMostLikely(self):
        likely = 0
        for i in self.likelihood:
            if self.likelihood[i] > likely:
                ans = i
                likely = self.likelihood[i]
        return ans
                    
                
                
    def updateWeights(self, answer, correct):
        #if correct is True:
        if answer in self.answers:
            for i in self.questionsUsed:
                plays = self.timesPlayed[answer][i]
                self.prevAnswers[answer][i] = self.prevAnswers[answer][i] * (float(plays) / float(plays + 1)) + float(self.answersGiven[i]) / float(plays)

                self.timesPlayed[answer][i] += 1

        else:
            for answer in self.answers:
                for i in self.questionsUsed:
                    self.prevAnswers[answer][i] = self.answersGiven[i]
                    self.timesPlayed[answer][i] = 1
                
        # we need to consider this part
        #else:
        #    for i in self.questionsUsed:
        #        if self.answers[answer][i] is 0:
        #            self.prevAnswers[answer][i] += 1
        #        self.timesPlayed[answer][i] += 1
    
    def askAnotherQuestion(self):
        if len(self.questions) > len(self.questionsUsed):
            possibleQ = list(range(0,len(self.questions)))
            remaining = list(set(possibleQ)-set(self.questionsUsed))
            self.questionsUsed.append(remaining[0])
            return self.questions[remaining[0]]
        else:
            return None
            
    
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
                    
        # copy prevAnswers to csv
        myfile = open('tempWeights.csv', 'w')
        with myfile:
            myFields = Qs
            writer = csv.DictWriter(myfile, fieldnames=myFields)    
            writer.writeheader()
            for i in self.prevAnswers:
                newlist = [i]
                for j in self.prevAnswers[i]:
                    newlist.append(j)
                writer.writerow({Qs[k]:newlist[k] for k in range(len(Qs))})
                
        myfile = open('timesPlayed.csv', 'w')
        with myfile:
            myFields = Qs
            writer = csv.DictWriter(myfile, fieldnames=myFields)    
            writer.writeheader()
            for i in self.timesPlayed:
                newlist = [i]
                for j in self.timesPlayed[i]:
                    newlist.append(j)
                writer.writerow({Qs[k]:newlist[k] for k in range(len(Qs))})
