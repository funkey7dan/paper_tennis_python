import random
from MinMaxPlayer import MinMax
from Player import Player
from game import Game

MAX_SCORE = 50
PLAY_TIMES = 100


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


if __name__ == '__main__':
    #p1 = MinMax(MAX_SCORE,load_cache = False,name = "agent2")
    p1 = Random("Ran2")
    #p1 = Human("Meatbag1")
    p2 = MinMax(MAX_SCORE,load_cache = True,name = "agent1")
    #p2 = Human("Meatbag2")
    p1.direction = -1
    p2.direction = 1
    g = Game(p1,p2,MAX_SCORE)
    g.battle(rounds = PLAY_TIMES)
    print("done")
