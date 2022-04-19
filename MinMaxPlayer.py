from Player import Player
import json

# its now this players turn to choose a number
class turn_state:

    def __init__(self,board_state,score_self,score_adv,direction,adv_play = None):
        self.board_state = board_state  #the state of the board - where the ball is on the field
        self.score_self = score_self  # the amount of points left to use
        self.score_adv = score_adv  # the amount of points adversary has to use
        self.adv_play = adv_play  # the number the adversary played
        self.game_state = 0  # -1 lost 1 won 0 neither
        self.plays_now = direction

def who_won(turn: turn_state):
    if turn.board_state == -3:
        return -1
    elif turn.board_state == 3:
        return 1
    if turn.score_self <= 0 or turn.score_adv <= 0:
        if turn.board_state < 0:
            return -1
        else:
            return 1
    return 0

class MinMax(Player):
    cache = {}
    def __init__(self,MAX_SCORE):
        # cache of game states - tuple of turn state and the optimal value to play
        # try:
        #     with open("data.json","r") as fp:
        #         self.cache = json.load(self.cache,fp)
        # except:
        #     self.cache = {}
        # super().__init__("MinMax",MAX_SCORE)
        super().__init__("MinMax",MAX_SCORE)

    def reset(self,MAX_SCORE):
        super().reset(MAX_SCORE)

    # the game evaluation from the position of the minimizing player, returns tuple of smallest value and move
    # leading to it
    def _min(self,turn: turn_state):
        if len(self.cache) != 0 and turn in self.cache:
            print(self.cache[turn])
            return self.cache[turn]
        min_value = 0  # neither win or loss
        move = -1  # -1 is no move
        # check if the game is won, and who won
        if who_won(turn) == turn.plays_now:
            # we won, return
            move = -1  #not a move, placeholder
            min_value = 1
        elif who_won(turn) == -turn.plays_now:
            move = -1
            min_value = -1
        else:
            for i in range(1,turn.score_self + 1):
                # see the board from the view of the opponent, if we played i
                updated_board = turn.board_state
                if turn.adv_play is not None:
                    # the number chosen is less than adversary, the one who plays now loses position
                    if i < turn.adv_play:
                        updated_board -= turn.plays_now
                    elif i > turn.adv_play:
                        updated_board += turn.plays_now
                next_turn = turn_state(board_state = updated_board,score_self = turn.score_adv,
                                       score_adv = turn.score_self - i,direction = -turn.plays_now,adv_play = i)
                res,move = self._max(next_turn)
                #finding the minimum
                if res < min_value or move == -1:
                    min_value = res
                    move = i

                    # if it's a loss, its the best outcome for us so we break
                    if min_value == -1:
                        self.cache[turn] = (min_value,move)
                        return min_value,move

        self.cache[turn] = (min_value,move)
        return min_value,move

        # the game evaluation from the position of the minimizing player, returns tuple of smallest value and move  #
        # leading to it

    def _max(self,turn: turn_state):
        if len(self.cache) != 0 and turn in self.cache:
            print(self.cache[turn])
            return self.cache[turn]
        max_value = 0  # initialize with neither win or loss
        move = -1  # -1 is no move
        # check if the game is won, and who won
        if who_won(turn) == turn.plays_now:
            # we won, return
            move = -1  #not a move, placeholder
            max_value = 1
        elif who_won(turn) == -turn.plays_now:
            move = -1
            max_value = -1
        else:
            for i in range(1,turn.score_self + 1):
                # see the board from the view of the opponent, if we played i
                updated_board = turn.board_state
                if turn.adv_play is not None:
                    # the number chosen is less than adversary, the one who plays now loses position
                    if i < turn.adv_play:
                        updated_board -= turn.plays_now
                    elif i > turn.adv_play:
                        updated_board += turn.plays_now
                next_turn = turn_state(board_state = updated_board,score_self = turn.score_adv,
                                       score_adv = turn.score_self - i,direction = -turn.plays_now,adv_play = i)
                res,move = self._min(next_turn) # result of choosing i
                #finding the maximum
                if res > max_value or move == -1:
                    max_value = res
                    move = i

                    # if it's a win, its the best outcome for us so we break
                    if max_value == 1:
                        self.cache[turn] = (max_value,move)
                        return max_value,move

        self.cache[turn] = (max_value,move)
        return max_value,move

    def calculate_move(self,turn: turn_state):
        outcome,move = self._max(turn)
        return str(max(move,1))

    # inherited from Player class
    def returnValue(self):
        move = self.calculate_move(
            turn = turn_state(board_state = self.game_state,score_self = self.score,score_adv = self.adv_score,
                              direction = self.direction,adv_play = self.adv_num))
        self.score -= int(move)
        return move

    def saveCache(self):
        with open("data.json","w") as fp:
            if (len(self.cache) > 0):
                json.dump(self.cache,fp)
