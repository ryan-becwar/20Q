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
        keepPlaying = True
        while keepPlaying:
            print("Welcome to 20 Questions!")

            print(self.game.getFirstQuestion())
            answer = self.game.convertAnswer(input())

            self.game.answerQuestion(self.game.questionsUsed[0], answer)

            i = 0
            while len(self.game.remainingFood) > 1:
                i += 1
                nextQ = self.game.getNextQuestion()
                if not nextQ:
                    break
                data = [(name, self.game.likelihood[name]) for name in self.game.remainingFood]
                print(data)
                print(nextQ)
                answer = self.game.convertAnswer(input())
                while answer == -1:
                    print(nextQ)
                    print("Please answer with 'yes' or 'no'.")
                    answer = self.game.convertAnswer(input())
                self.game.answerQuestion(self.game.questionsUsed[i], answer)

            #selected = self.game.remainingFood[0]
            data = [(name, self.game.likelihood[name]) for name in self.game.remainingFood]
            selected = max(data, key=lambda item:item[1])[0]

            print(data)
            print("Are you thinking of", selected, "?")
            correct = self.game.convertAnswer(input())

            if correct == 0:
                print("Enter the name of the object you are thinking of:")
                correctAnswer = input()
                
                if correctAnswer not in list(self.game.answers):
                    print("Please help me learn about", correctAnswer,"by answering a few more questions.")
                    self.getRemainingUnanswered()

                self.game.updateWeights(correctAnswer, False)

            else:
                self.game.updateWeights(selected, True)

            self.game.resetGame()
            print("Would you like to keep playing?")
            answer = self.game.convertAnswer(input())
            if answer != 1:
                keepPlaying = False

if __name__ == "__main__":
    ui = UI()
    ui.playGame()
