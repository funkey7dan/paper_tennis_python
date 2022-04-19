import random
from MinMaxPlayer import MinMax
from Player import Player

MAX_SCORE = 50
PLAY_TIMES = 10000

score1 = MAX_SCORE
score2 = MAX_SCORE
prevState = 0
state = 0
end = False

class Human(Player):
    def __init__(self,name):
        super().__init__(name,MAX_SCORE)

    def returnValue(self):
        self.self_num = input()
        #self.score -= int(self.self_num)
        return self.self_num

class Random(Player):

    def __init__(self,name):
        super().__init__(name,MAX_SCORE)

    def returnValue(self):
        random_num = -1
        while random_num > self.score or random_num < 0:
            random_num = random.randint(1,self.score)
        self.self_num = random_num
        #self.score -= self.self_num
        print("")
        return str(self.self_num)

def init():
    global score2,score1
    print(p1.name + ": " + str(score1) + "         " + p2.name + ": " + str(score2) + " ")
    print(" --------------------------------- \n"
          " |       |       #       |       | \n"
          " |       |       #       |       | \n"
          " |       |       O       |       | \n"
          " |       |       #       |       | \n"
          " |       |       #       |       | \n"
          " --------------------------------- \n")

def drawBoard():
    global state
    print(p1.name + ": " + str(score1) + "         " + p2.name + ": " + str(score2) + " ")
    print(" --------------------------------- \n"
          " |       |       #       |       | \n"
          " |       |       #       |       | ")
    if (state == 0 and prevState == -1) or state == 1:
        print(" |       |       #   O   |       | ")
    if (state == 0 and prevState == 1) or state == -1:
        print(" |       |   O   #       |       | ")
    if state == 0 and prevState == 0:
        print(" |       |       O       |       | ")
    if state == -3:
        print("O|       |       #       |       | ")
    if state == 3:
        print(" |       |       #       |       |O")
    if state == -2:
        print(" |   O   |       #       |       | ")
    if state == 2:
        print(" |       |       #       |   O   | ")

    print(" |       |       #       |       | \n"
          " |       |       #       |       | \n"
          " --------------------------------- \n")

def check_win_cond(p1,p2):
    global end,score1,score2,prevState,state
    # if the ball is in the court of p2
    # or if player 2 still has points while player 1 not
    if state == -3 or (score1 <= 0 and score2 > 0):
        print(p2.name + " WINS !")
        print(" --------------------------------- ")
        p1.set_win(False)
        p2.set_win(True)
        end = True
        return
    # if the ball is in the court of p1
    # or if player 1 still has points while player 2 not
    if state == 3 or (score2 <= 0 and score1 > 0):
        print(p1.name + " WINS !")
        print(" --------------------------------- ")
        p1.set_win(True)
        p2.set_win(False)
        end = True
        return
    # if both are 0
    elif score1 <= 0 and score2 <= 0:
        if state < 0:
            print(p2.name + " WINS !")
            print(" --------------------------------- ")
            p1.set_win(False)
            p2.set_win(True)
            end = True
            return
        elif state > 0:
            print(p1.name + " WINS !")
            print(" --------------------------------- ")
            p2.set_win(False)
            p1.set_win(True)
            end = True
            return
        else:
            print("IT'S A DRAW !")
            print(" --------------------------------- ")
            p2.set_win(False)
            p1.set_win(False)
            end = True
            return

def check_state(num1,num2):
    global end,score1,score2,prevState,state
    score1 -= num1
    score2 -= num2
    prevState = state
    if num1 > num2:
        state += 1
    elif num1 < num2:
        state -= 1

def playTurn(p1,p2):
    global end,score1,score2,prevState
    while True:
        print(p1.name + " enter a number: ",end = '')
        num1 = p1.returnValue()
        if num1.isdecimal() and score1 >= int(num1) > 0:
            num1 = int(num1)
            p2.adv_num = num1
            p2.adv_score -= num1
            p1.score -= num1
            break
        print(p1.name + " " + num1 + " is NOT A VALID MOVE !")
    while True:
        print(p2.name + " enter a number: ",end = '')
        num2 = p2.returnValue()
        if num2.isdecimal() and score2 >= int(num2) > 0:
            num2 = int(num2)
            p1.adv_num = num2
            p1.adv_score -= num2
            p2.score -= num2
            break
        print(p2.name + " " + num2 + " is NOT A VALID MOVE !")
    print("\n")
    # pass advesary values to the players
    p1.getPlay(score2,num2,state)
    p2.getPlay(score1,num1,state)
    check_state(num1,num2)
    drawBoard()
    print("       " + p1.name + " played: " + str(num1) + "\n       " + p2.name + " played: " + str(num2) + "\n\n")

def playGame(p1,p2):
    global end,score1,score2,prevState
    init()
    while True:
        check_win_cond(p1,p2)
        if end:
            break
        playTurn(p1,p2)


def battle(p1: Player,p2: Player,rounds: int):
    for i in range(rounds):
        gameReset()
        p1.reset(MAX_SCORE)
        p2.reset(MAX_SCORE)
        playGame(p1,p2)
    print(p1.name + ": " + str(p1.wins),p2.name + ": " + str(p2.wins))
    if isinstance(p1,MinMax):
        p1.saveCache()
    if isinstance(p2,MinMax):
        p2.saveCache()


def gameReset():

    global state,prevState,score1,score2,end
    prevState = state = 0
    score1 = score2 = MAX_SCORE
    end = False


if __name__ == '__main__':
    #p1 = MinMax(MAX_SCORE,load_cache = False,name = "agent2")
    p1 = Random("Ran2")
    #p1 = Human("Meatbag")
    p2 = MinMax(MAX_SCORE,load_cache = True,name = "agent1")
    p1.direction = -1
    p2.direction = 1

    battle(p1,p2,PLAY_TIMES)
