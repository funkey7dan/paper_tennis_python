
class Game:

    def __init__(self,p1,p2,score):
        self.p1 = p1
        self.p2 = p2
        self.MAX_SCORE = score
        self.score1 = self.MAX_SCORE
        self.score2 = self.MAX_SCORE
        self.end = False
        self.prevState = 0
        self.state = 0

    def init(self):
        print(self.p1.name + ": " + str(self.score1) + "         " + self.p2.name + ": " + str(self.score2) + " ")
        print(" --------------------------------- \n"
              " |       |       #       |       | \n"
              " |       |       #       |       | \n"
              " |       |       O       |       | \n"
              " |       |       #       |       | \n"
              " |       |       #       |       | \n"
              " --------------------------------- \n")

    def draw_board(self):
        state = self.state
        prev_state = self.prevState
        print(self.p1.name + ": " + str(self.score1) + "         " + self.p2.name + ": " + str(self.score2) + " ")
        print(" --------------------------------- \n"
              " |       |       #       |       | \n"
              " |       |       #       |       | ")
        if state == 0 and prev_state == 0:
            print(" |       |       O       |       | ")
        elif (state == 0 and prev_state == -1) or state == 1:
            print(" |       |       #   O   |       | ")
            self.state = 1
        elif state == 2:
            print(" |       |       #       |   O   | ")
        elif state == 3:
            print(" |       |       #       |       |O")
        elif (state == 0 and prev_state == 1) or state == -1:
            print(" |       |   O   #       |       | ")
            self.state = -1
        elif state == -2:
            print(" |   O   |       #       |       | ")
        elif state == -3:
            print("O|       |       #       |       | ")
        print(" |       |       #       |       | \n"
              " |       |       #       |       | \n"
              " --------------------------------- \n")

    @staticmethod
    def check_win_cond(score1 = None,score2 = None,state = None):
        # if not score1:
        #     score1 = self.score1
        # if not score2:
        #     score2 = self.score2
        # if not state_par:
        #     state = self.state
        # else:
        #     state = state_par

        # if the ball is in the court of self.p2
        # or if player 2 still has points while player 1 not
        if state == -3 or (score1 <= 0 and score2 > 0):
            return 1
        # if the ball is in the court of p1
        # or if player 1 still has points while player 2 not
        if state == 3 or (score2 <= 0 and score1 > 0):
            return -1
        # if both have 0 points the one who loses is the one with the ball on his field
        elif score1 <= 0 and score2 <= 0:
            if state < 0:
                return 1
            elif state > 0:
                return -1
            else:
                return 0

    def announce_winner(self,player):
        if player is not None:
            if player == 1:
                print(self.p2.name + " WINS !")
                print(" --------------------------------- ")
                self.p2.set_win(True)
                self.p1.set_win(False)

            if player == -1:
                print(self.p1.name + " WINS !")
                print(" --------------------------------- ")
                self.p1.set_win(True)
                self.p2.set_win(False)

            if player == 0:
                print("IT'S A DRAW !")
                print(" --------------------------------- ")
                self.p2.set_win(False)
                self.p1.set_win(False)
            self.end = True
            return

    def check_state(self,num1,num2):

        self.score1 -= num1
        self.score2 -= num2
        self.prevState = self.state
        if num1 > num2:
            self.state += 1
        elif num1 < num2:
            self.state -= 1

    @staticmethod
    def get_number(player,adversary):
        while True:
            print(player.name + " enter a number: ",end = '')
            num1 = player.returnValue()
            if num1.isdecimal() and player.score >= int(num1) > 0:
                num1 = int(num1)
                adversary.adv_num = num1
                adversary.adv_score -= num1
                player.score -= num1
                return num1
            print(player.name + " " + num1 + " is NOT A VALID MOVE !")

    def play_turn(self):
        state = self.state
        num1 = self.get_number(self.p1,self.p2)
        num2 = self.get_number(self.p2,self.p1)
        print("\n")
        # pass adversary values to the players
        self.p1.getPlay(self.score2,num2,state)
        self.p2.getPlay(self.score1,num1,state)
        self.check_state(num1,num2)
        self.draw_board()
        print("       " + self.p1.name + " played: " + str(num1) + "\n       " + self.p2.name + " played: " + str(
            num2) + "\n\n")

    def play_game(self):
        self.init()
        while True:
            self.announce_winner(self.check_win_cond(self.score1,self.score2,self.state))
            if self.end:
                break
            self.play_turn()

    def battle(self,rounds: int):
        for i in range(rounds):
            self.game_reset()
            self.p1.reset(self.MAX_SCORE)
            self.p2.reset(self.MAX_SCORE)
            self.play_game()
        print(self.p1.name + ": " + str(self.p1.wins),self.p2.name + ": " + str(self.p2.wins))
        try:
            self.p1.saveCache()
        except:
            pass

        try:
            self.p2.saveCache()
        except:
            pass

    def game_reset(self):

        self.prevState = self.state = 0
        self.score1 = self.score2 = self.MAX_SCORE
        self.end = False
