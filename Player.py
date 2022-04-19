class Player:

    def __init__(self,name,MAX_SCORE):
        self.adv_num = None
        self.self_num = None
        self.win_state = None
        self.adv_score = MAX_SCORE
        self.name = name
        self.score = MAX_SCORE
        self.game_state = 0
        self.wins = 0
        self.games = 0
        self.direction = 0 # if left or right player

    def reset(self,MAX_SCORE):
        self.adv_num = None
        self.self_num = None
        self.win_state = None
        self.adv_score = MAX_SCORE
        self.score = MAX_SCORE
        self.game_state = 0

    def returnValue(self):
        pass

    def getPlay(self,adv_score,adv_num,g_state):
        self.adv_score = adv_score
        self.adv_num = adv_num
        self.game_state = g_state

    def set_win(self,win_state = None):
        self.win_state = win_state
        self.games += 1
        if win_state: self.wins += 1