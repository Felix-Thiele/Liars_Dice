from random import randint

class bluff_gamestate:
    """
    This class describes the gamestate of bluff
    It consists of:
        - players: list of functions describing strategies given the gamestate
        - dice_nr: list of number of dice that each player has
        - dice: the rolled dice for each player
        - history: the history of moves since the last bluff was called
        - state: the current bet. This is a touple, the first value for the number, and the second for the face.
                The moves will be of the same form. A bluff is encoded by (1,0).
        - active player: the index of the current player
        - possible states: 'higher' defines a total ordering on the states(moves). In possible states all possible states
                            are saved in the ordering defined by higher.
    players may use public functions of gamestate.
    """
    def __init__(self, players=[], bluff_rules=1, verbose=False):
        self.players = players
        self.dice_nr = [5 for _ in range(len(players))]
        self._dice =  []
        self._roll_dice()
        self.history = []
        self.state = (1,0)
        self.active_player = 0
        self.verbose = verbose

        if bluff_rules == 1:
            self._bluff_rules = self._bluff_rules_1
        elif bluff_rules == 2:
            self._bluff_rules = self._bluff_rules_2
        else:
            raise ValueError('This bluff rule is not implemented')


        self.possible_states = {}
        _i, _temp_state = 0, (1,0)
        while _temp_state!= None:
            self.possible_states[_temp_state] = _i
            _temp_state = self.get_next_state(_temp_state)
            _i+=1

    def _bluff_rules_1(self, diff):
        if 0 > diff:
            self.dice_nr[self.active_player] -= diff
        else:
            for index in range(len(self.players)):
                if index != self.active_player:
                    self.dice_nr[index] -= (diff + 1)

    def _bluff_rules_2(self, diff):
        if 0 > diff:
            self.dice_nr[self.active_player] -= 1
        else:
            for index in range(len(self.players)):
                if index != self.active_player:
                    self.dice_nr[index] -= 1

    def _roll_dice(self):
        # Rolls the dice of each player
        self._dice = [[randint(1, 6) for _ in range(self.dice_nr[index])] for index in range(len(self.players))]


    @staticmethod
    def get_next_state(state):
        #
        if state == (1,0):
            return 0, 1
        if state[0] == 20 and state[1]==5:
            return None
        elif state[1] < 5:
            return state[0], state[1] + 1
        elif state[1] == 5:
            if state[0] % 2 == 0:
                return state[0] + 1, 1
            return (state[0] + 1) // 2, 6
        elif state[1] == 6:
            return state[0] * 2, 1


    def get_my_dice(self):
        return self._dice[self.active_player]

    def move_is_legal(self, move):
        if move == (1,0):
            return True
        if self.possible_states[self.state]< self.possible_states[move]:
            return True
        return False

    def move(self, move):
        assert self.move_is_legal(move)
        self.history.append([self.active_player, move])
        if move == (1,0):
            self.history = []
            all_dice = [die for pl_dice in self._dice for die in pl_dice]
            diff = self.state[0]-all_dice.count(6)+all_dice.count(self.state[1])
            self._bluff_rules(diff)
            self._roll_dice()
        else:
            self.state = move

        # check if game over or pick next active player
        if sum(1 for _ in self.dice_nr if _ > 0)>1:
            self.active_player = (self.active_player+1)%len(self.players)
            while self.dice_nr[self.active_player] <= 0:
                self.active_player = (self.active_player+1)%len(self.players)
        else:
            if self.verbose:
                print('Player: ',self.get_winner(), ' won!!!')
            return False
        return True

    def play_game(self):
        game_live = True
        while game_live:
            game_live = self.move(self.players[self.active_player](self))
        return self.get_winner()

    def get_winner(self):
        winner = 0
        while self.dice_nr[winner] <= 0:
            winner += 1
        return winner
