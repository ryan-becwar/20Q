from twentyQ import *

class UI:
    def __init__(self):
        self.game = twentyQ()
        
    def getRemainingUnanswered(self):
        i = len(self.game.questionsUsed)
        nextQ = self.game.askAnotherQuestion()
        while nextQ != None:
            print(nextQ)
            answer = self.game.convertAnswer(input())
            while answer == -1:
                print(nextQ)
                print("Please answer with 'yes' or 'no'.")
                answer = self.game.convertAnswer(input())
            self.game.answerQuestion(self.game.questionsUsed[i], answer)
            nextQ = self.game.askAnotherQuestion()
            i+=1

    def playGame(self):
        print("Welcome to 20 Questions!")

        print(self.game.getFirstQuestion())
        answer = self.game.convertAnswer(input())

        self.game.answerQuestion(self.game.questionsUsed[0], answer)

        i = 0
        while len(self.game.remainingFood) > 1 and i < 10:
            i += 1
            nextQ = self.game.getNextQuestion()
            if not nextQ:
                break
            print(nextQ)
            answer = self.game.convertAnswer(input())
            while answer == -1:
                print(nextQ)
                print("Please answer with 'yes' or 'no'.")
                answer = self.game.convertAnswer(input())
                
            self.game.answerQuestion(self.game.questionsUsed[i], answer)

        selected = self.game.getMostLikely()
        print("Is", selected,"what you are thinking of?")
        correct = self.game.convertAnswer(input())

        if correct == 0:
            print("Enter the name of the object you are thinking of:")
            correctAnswer = input()
            
            if correctAnswer not in list(self.game.answers):
                self.getRemainingUnanswered()

            self.game.updateWeights(correctAnswer, False)

        else:
            self.game.updateWeights(correct, True)

if __name__ == "__main__":
    ui = UI()
    ui.playGame()
