import random
from random import randint
import numpy as np
from tqdm import tqdm

class bluff_gamestate:
    """
    This class describes the gamestate of bluff
    It consists of:
        - players: list of functions describing strategies given the gamestate
        - dice_nr: list of number of dice that each player has
        - dice: the rolled dice for each player
        - history: the history of moves since the last bluff was called
        - state: the current bet. This is a touple, the first value for the number, and the second for the face.
                The moves will be of the same form. A bluff is encoded by (0,5). The beginning state is (1,0)
        - active player: the index of the current player
        - possible states: 'higher' defines a total ordering on the states(moves). In possible states all possible states
                            are saved in the ordering defined by higher.
    players may use public functions of gamestate.
    """

    def __init__(self, players=[], bluff_rules=1):

        self.list_possible_states = []
        self.possible_states = {}
        _i, _temp_state = 0, (1, 0)
        while _temp_state != None:
            self.list_possible_states.append(_temp_state)
            self.possible_states[_temp_state] = _i
            _temp_state = self._get_next_state(_temp_state)
            _i += 1

        self.players = players
        self.dice_nr = np.array([5 for _ in range(len(players))])
        self._dice = []
        self._roll_dice()
        self.state = (1, 0)
        self.last_to_move = random.randint(0,len(self.players)-1)
        self.next_to_move = (self.last_to_move+1)%len(self.players)


        self.history_hash = np.array([0] * (len(self.list_possible_states) - 1))
        self.history = []
        if bluff_rules == 1:
            self._bluff_rules = self._bluff_rules_1
        elif bluff_rules == 2:
            self._bluff_rules = self._bluff_rules_2
        else:
            raise ValueError('This bluff rule is not implemented')

    def reset(self):
        self.dice_nr = np.array([5 for _ in range(len(self.players))])
        self._dice = []
        self._roll_dice()
        self.history_hash = np.array([0] * (len(self.list_possible_states) - 1))
        self.history = []
        self.state = (1, 0)
        self.last_to_move = random.randint(0,len(self.players)-1)
        self.next_to_move = (self.last_to_move+1)%len(self.players)

    def get_my_dice(self):
        return self._dice[self.next_to_move]

    def move_is_legal(self, move):
        if move == (0, 5) and self.state not in [(1, 0), (0, 5)]:
            return True
        if self.possible_states[self.state] < self.possible_states[move]:
            return True
        return False

    def move(self, move):
        assert self.move_is_legal(move), (move, ' is not legal move for ', self.state)
        self.history_hash[self.possible_states[move] - 1] = 1
        self.history.append([self.next_to_move, move])
        if move == (0, 5):
            all_dice = [die for pl_dice in self._dice for die in pl_dice]
            # if diff is positive then the last bet was wrong
            diff = self.state[0] - all_dice.count(6) - all_dice.count(self.state[1])
            self._bluff_rules(diff)
            self._roll_dice()
            self.history_hash = np.array([0] * (len(self.list_possible_states) - 1))
            self.history=[]
        self.state = move if move != (0, 5) else (1, 0)

        # check if game over or pick next active player
        if sum(1 for _ in self.dice_nr if _ > 0) > 1:
            self.next_to_move = (self.next_to_move + 1) % len(self.players)
            while self.dice_nr[self.next_to_move] <= 0:
                self.next_to_move = (self.next_to_move + 1) % len(self.players)
                self.last_to_move = self.next_to_move
        else:
            return False
        return True

    def play_game(self, return_train=False):
        game_live = True
        while game_live:
            move = self.players[self.next_to_move](self)
            game_live = self.move(move)
        return self._get_winner()


    def collect_data(self, ammount):
        # todo need better scoring, also track if won or not... 1, -1, 0.2 just for some basic testing
        x, y = [], []
        for _ in range(ammount):
            game_live = True
            while game_live:
                next_move = self.players[self.next_to_move](self)

                x.append(self.get_encoding())
                if next_move == (0, 5):
                    all_dice = [die for pl_dice in self._dice for die in pl_dice]
                    # if diff is positive then the last bet was wrong
                    diff = self.state[0] - all_dice.count(6) - all_dice.count(self.state[1])
                    if diff > 0:
                        y.append(1)
                    else:
                        y.append(-1)
                else:
                    y.append(0)
                game_live = self.move(next_move)
            self.reset()
        return np.array(x), np.array(y)


    def _get_winner(self):
        winner = 0
        while self.dice_nr[winner] <= 0:
            winner += 1
        return winner

    def get_encoding(self, last_next=False, hash_sorted_dice=False, hash_max_players=10):
        p = self.last_to_move
        if last_next:
            p = self.next_to_move
        game_encoding = []
        dice = self._dice[p] if hash_sorted_dice else sorted(self._dice[p])
        for die in dice:
            game_encoding += [0] * (die - 1) + [1] + [0] * (6 - die)
        game_encoding += [0]*6*(5-max(0,self.dice_nr[p]))
        game_encoding += [0] * (len(self.players) - 2) + [1] + [0] * (hash_max_players - 2 - len(self.players))
        return np.concatenate((np.array(game_encoding), self.history_hash))

    def _roll_dice(self):
        # Rolls the dice of each player
        self._dice = [[randint(1, 6) for _ in range(self.dice_nr[index])] for index in range(len(self.players))]

    @staticmethod
    def _get_next_state(state):
        #
        if state == (0, 5):
            return None
        if state[0] == 20 and state[1] == 5:
            return (0, 5)
        elif state[1] < 5:
            return state[0], state[1] + 1
        elif state[1] == 5:
            if state[0] % 2 == 0:
                return state[0] + 1, 1
            return (state[0] + 1) // 2, 6
        elif state[1] == 6:
            return state[0] * 2, 1

    def _bluff_rules_1(self, diff):
        if 0 > diff:
            self.dice_nr[self.next_to_move] += diff
        else:
            for index in range(len(self.players)):
                if index != self.next_to_move:
                    self.dice_nr[index] -= (diff + 1)

    def _bluff_rules_2(self, diff):
        if 0 > diff:
            self.dice_nr[self.next_to_move] -= 1
        else:
            for index in range(len(self.players)):
                if index != self.next_to_move:
                    self.dice_nr[index] -= 1


