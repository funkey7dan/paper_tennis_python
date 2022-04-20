from Player import Player
from game import Game
import json

REC_DEPTH = 9999
# its now this players turn to choose a number
class turn_state:
    hash = None

    def __init__(self,board_state,score_self,score_adv,direction,adv_play = None):
        self.board_state = board_state  #the state of the board - where the ball is on the field
        self.score_self = score_self  # the amount of points left to use
        self.score_adv = score_adv  # the amount of points adversary has to use
        self.adv_play = adv_play  # the number the adversary played
        self.game_state = 0  # -1 lost 1 won 0 neither
        self.plays_now = direction
        #self.agent_type = agent_type

    def get_hash(self):
        if self.hash:
            return self.hash
        hash_value = ''
        for a in self.__dict__.values():
            a = str(a)
            hash_value += a + '_'
        #print(hash_value)
        self.hash = hash_value
        # board state | self_score | adversary score | number adv played | state of the game| direction | agent type
        return hash_value

def who_won(turn: turn_state):
    if turn.plays_now == -1:
        return Game.check_win_cond(score1 = turn.score_self,score2 = turn.score_adv,state = turn.board_state)
    else:
        return Game.check_win_cond(score2 = turn.score_self,score1 = turn.score_adv,state = turn.board_state)

class MinMax(Player):
    # how many recursion levels we allow
    cache = {}
    debug_cache = {}

    def __init__(self,MAX_SCORE,load_cache,name = "MinMax"):
        # cache of game states - tuple of turn state and the optimal value to play
        self.load_cache = load_cache
        if load_cache:
            try:
                with open(name + "data.json","r") as fp:
                    self.cache = json.load(fp)
            except Exception as e:
                print(e)
                self.cache = {}
        super().__init__(name,MAX_SCORE)

    def reset(self,MAX_SCORE):
        super().reset(MAX_SCORE)

    # the game evaluation from the position of the minimizing player, returns tuple of smallest value and move
    # leading to it
    def _min(self,turn: turn_state,depth: int = 0):
        if depth >= REC_DEPTH:
            return turn.board_state,-1
        # set the value of winning for current player
        WIN_STATE = 3 * turn.plays_now
        LOSE_STATE = WIN_STATE
        if len(self.cache) != 0 and turn.get_hash() in self.cache:
            #print(self.cache[hash(turn)])
            self.debug_cache[turn.get_hash()] = turn
            if turn.score_self >= self.cache[turn.get_hash()][1]:
                #print("debug")
                return self.cache[turn.get_hash()]
        min_value = 0  # neither win or loss
        move = -1  # -1 is no move
        # check if the game is won, and who won
        winner = who_won(turn)
        if winner == turn.plays_now:
            # we won, return
            move = -1  #not a move, placeholder
            min_value = WIN_STATE
        elif winner == -turn.plays_now:
            move = -1
            min_value = LOSE_STATE
        else:
            for j in range(1,turn.score_self + 1):
                # see the board from the view of the opponent, if we played i
                updated_board = turn.board_state
                if turn.adv_play is not None:
                    # the number chosen is less than adversary, the one who plays now loses position
                    if j < turn.adv_play:
                        updated_board -= turn.plays_now
                    elif j > turn.adv_play:
                        updated_board += turn.plays_now
                next_turn = turn_state(board_state = updated_board,score_self = turn.score_adv,
                                       score_adv = turn.score_self - j,direction = -turn.plays_now,
                                       adv_play = None)
                res,move = self._max(next_turn,depth = depth + 1)

                #finding the minimum
                if res < min_value or move == -1:
                    min_value = res
                    move = j

                # if it's a loss, its the lowest outcome for us so we break
                if min_value == LOSE_STATE:
                    self.cache[turn.get_hash()] = (min_value,move)
                    return min_value,move

        self.cache[turn.get_hash()] = (min_value,move)
        return min_value,move

        # the game evaluation from the position of the minimizing player, returns tuple of smallest value and move  #
        # leading to it

    def _max(self,turn: turn_state,depth: int = 0):
        if depth >= REC_DEPTH:
            return turn.board_state,-1
        # set the value of winning for current player
        WIN_STATE = 3 * turn.plays_now
        LOSE_STATE = -WIN_STATE
        if len(self.cache) != 0 and turn.get_hash() in self.cache:
            #print(self.cache[hash(turn)])
            self.debug_cache[turn.get_hash()] = turn
            if turn.score_self >= self.cache[turn.get_hash()][1]:
                return self.cache[turn.get_hash()]
        max_value = 0  # initialize with neither win or loss
        move = -1  # -1 is no move

        # check if the game is won, and who won
        if who_won(turn) == turn.plays_now:
            # we won, return
            move = -1  #not a move, placeholder
            max_value = WIN_STATE
        elif who_won(turn) == -turn.plays_now:
            move = -1
            max_value = LOSE_STATE

        else:
            for i in range(1,turn.score_self + 1):
                # see the board from the view of the opponent, if we played i
                updated_board = turn.board_state
                # if adversary already played
                if turn.adv_play is not None:
                    # the number chosen is less than adversary, the one who plays now loses position
                    if i < turn.adv_play:
                        updated_board -= turn.plays_now
                    elif i > turn.adv_play:
                        updated_board += turn.plays_now
                #pass to the minimizing agent the next state, with the values according to the choice i
                next_turn = turn_state(board_state = updated_board,score_self = turn.score_adv,
                                       score_adv = turn.score_self - i,direction = -turn.plays_now,adv_play = i)
                res,move = self._min(next_turn,depth = depth + 1)  # result of choosing i
                #finding the maximum:
                # if it's a win, its the best outcome for us so we break
                #update the new maximum if larger
                if res > max_value or move == -1:
                    max_value = res
                    # the current i is the best move
                    move = i

                if max_value == WIN_STATE:
                    self.cache[turn.get_hash()] = (max_value,move)
                    return max_value,move
        self.cache[turn.get_hash()] = (max_value,move)
        return max_value,move

    def calculate_move(self,turn: turn_state):

        outcome,move = self._max(turn)
        return str(max(move,1))

    # inherited from Player class
    def returnValue(self):
        move = self.calculate_move(
            turn = turn_state(board_state = self.game_state,score_self = self.score,score_adv = self.adv_score,
                              direction = self.direction,adv_play = self.adv_num))
        print("")
        return move

    def saveCache(self):
        if self.load_cache:
            with open(self.name + "data.json","w") as fp:
                if len(self.cache) > 0:
                    #fp.seek(0)
                    json.dump(self.cache,fp)
