from twentyQ import *

class UI:
    def __init__(self):
        self.game = twentyQ()

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

        print("Is", self.game.getMostLikely(), "what you are thinking of?")

if __name__ == "__main__":
    ui = UI()
    ui.playGame()
