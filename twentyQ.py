
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
        for j in range(0,len(self.questions)):
            for i in self.answers:
                if self.answers[i][j] == 1:
                    countYes = countYes + 1
                elif self.answers[i][j] == -1:
                    countNo = countNo + 1
            nextQ.append(abs(countYes - countNo))
            countYes = countNo = 0
        self.questionsUsed.append(self.questions[np.argmin(nextQ)])
        return self.questions[np.argmin(nextQ)]
            
    def getNextQuestion(self, currentQ, currentA):
        couldBe = []
        countYes = 0
        countNo = 0
        nextQ = []
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
        self.questionsUsed.append(self.questions[np.argmin(nextQ)])
        return self.questions[np.argmin(nextQ)]
    
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
                self.likelihood[i] = self.likelihood[i] + self.weightVals[i][self.questions.index(currentQ)] *1
            else:
                self.likelihood[i] = self.likelihood[i] + self.weightVals[i][self.questions.index(currentQ)] *-1
                
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
        data = pd.read_csv('tempData.csv')

        # get weights from csv
        weights = pd.read_csv('tempWeights.csv')