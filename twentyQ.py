import numpy as np
import pandas as pd
import csv
import copy as cp
import random

THRESHOLD = 1.8

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

    def resetGame(self):
        self.__init__()
        
    #Get the next question which divides the set of "remaining" answers the most
    def getNextQuestion(self):
        nextQ = []
        possibleQ = []
        for j in range(0,len(self.questions)):
            questionSum = 0
            decisiveScore = 0
            for i in self.remainingFood:
                questionSum += self.prevAnswers[i][j]
                #score to determine decisive answers to the question are
                decisiveScore += .5 - abs(self.prevAnswers[i][j] - .5)
            #score to determine how much the question divides the dataset
            dividingScore = abs(questionSum - float(len(self.remainingFood)) / 2)

            #aggregate of two scores
            nextQ.append(dividingScore + 0.8*decisiveScore)
            
        unused = list(set(range(len(nextQ))) - set(self.questionsUsed))
        unusedVals = list(nextQ[x] for x in unused)
        if not unusedVals:
            return None
        minVal = min(unusedVals)

        for i in unused:
            if nextQ[i] == minVal:
                possibleQ.append(i)
                
        if possibleQ:
            choice = random.choice(possibleQ)
            self.questionsUsed.append(choice)
            return self.questions[choice]
        else:
            return None
    
    def answerQuestion(self, currentQ, currentA):
        self.updateLikelihood(currentQ, currentA)

        #select all answers which have a likelihood within THRESHOLD of the maxlikelihood
        self.remainingFood = list(k for k, v in self.likelihood.items() if v >= max(self.likelihood.values()) - THRESHOLD)

    def convertAnswer(self, currentA):
        if currentA == 'yes' or currentA == 'y':
            return 1
        elif currentA == 'no' or currentA == 'n':
            return 0
        elif currentA == 'sometimes' or currentA == 'maybe' or currentA == 'unknown' or currentA == 's':
            return 0.5
        else:
            return -1
        
    def updateLikelihood(self, currentQ, currentA):
        #append the answer
        self.answersGiven.append(currentA)
        
        #using weights from prevAnswers:
        for ans in self.prevAnswers:
            self.likelihood[ans] += 1 - abs(currentA - self.prevAnswers[ans][currentQ])
                    
                
                
    def updateWeights(self, answer):
        if answer in self.prevAnswers:
            for i in self.questionsUsed:
                plays = self.timesPlayed[answer][i]
                self.prevAnswers[answer][i] = self.prevAnswers[answer][i] * (float(plays) / float(plays + 1)) + float(self.answersGiven[self.questionsUsed.index(i)]) / float(plays + 1)

                self.timesPlayed[answer][i] += 1

        else:
            self.prevAnswers[answer] = []
            self.timesPlayed[answer] = []
            self.answers[answer] = []
            for i in range(len(self.questions)):
                #if the index shows up in the asked questions:
                if i in self.questionsUsed:
                    #answersGiven is a list of only asked questions, so we need to look up the index from questionsUsed
                    self.prevAnswers[answer].append(self.answersGiven[self.questionsUsed.index(i)])
                    self.answers[answer].append(self.answersGiven[self.questionsUsed.index(i)])
                    self.timesPlayed[answer].append(1)
                else:
                    self.prevAnswers[answer].append(0.5)
                    self.answers[answer].append(-1)
                    self.timesPlayed[answer].append(0)
                
        self.writeToCSV()
    
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
