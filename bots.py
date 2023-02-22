import random

import bluff
import numpy as np
import math

'''
Here some player agents are implemented.
Some more Ideas for Bots:
    - Depending on the payoff if it is preferred to become second, in the rule set that all players but the better
        have to pay for wrong bluff calls, one might try to purposefully kick out a player who has less dice, by
        calling a bluff on plays that are below the expectation.
    - One of the bots here tries to guess when players have 1 more than the expectation of a certain face. 
        This is done when a player bets above the expectation. But one could go one step further since other players might
        have also guessed that a third player has more than the expectation and only be using this information for his bet.
        Also if another player uses this tactic, one might approximate his expectations more accurately knowing one's own
        bets and dice.
    - It would be interesting to train a reinforcement algoirthm to see the differences to these strategies.
'''

def human_move(game):
    # either input FINAL_MOVE or two ints seperated by a comma
    print('\n\n\n\n--------------')
    print(game.dice_nr)
    for h in game.history:
        print('Player ', h[0], ' played move ', h[1])
    input1 = input('                 Input a move as two ints separated by a comma: ')
    return int(input1.split(',')[0]), int(input1.split(',')[1])


def random_bot(game):
    state = game._get_next_state(game.state)
    possible = []
    while state is not None:
        possible.append(state)
        state = game._get_next_state(state)
    return random.choice(possible)

def _get_move_from_expectationis(game, my_exp, bluff=0):

    state_likelyhoods = {(0, 5): -(my_exp[game.state[1] - 1] - game.state[0])} if game.state != (0, 5) else {}
    state = game._get_next_state(game.state)
    while state is not None:
        state_likelyhoods[state] = my_exp[state[1] - 1] - state[0]
        state = game._get_next_state(state)

    filt_lieklyhoods = {k: v + bluff for k, v in state_likelyhoods.items() if v + bluff > 0}
    if filt_lieklyhoods == {}:
        if state_likelyhoods == {}:
            return (0, 5)
        return list(state_likelyhoods.keys())[
            list(state_likelyhoods.values()).index(max(list(state_likelyhoods.values())))]

    vals, keys = list(filt_lieklyhoods.values()), list(filt_lieklyhoods.keys())
    l_sum = sum(vals)
    probability = [item / l_sum for item in vals]
    result = np.random.choice([i for i in range(len(vals))], 1, p=probability)[0]
    return list(keys)[result]

def bot_best_expectation(game, bluff=0):
    # This bot picks moves according to probabilities proportional to the difference between bet and expectation if positive
    # If all moves have negative expectation it calls a bluff.
    # The bluff value shifts is added to the expetation differences, so that the bot blluffs sometimes
    
    my_exp = [game.get_my_dice().count(i) 
              + game.get_my_dice().count(6)
              + (2 - i // 6) / 6 * (np.sum(game.dice_nr) - len(game.get_my_dice()))
              for i in range(1, 7)]

    return _get_move_from_expectationis(game, my_exp, bluff)


def bot_best_expectation_with_hist(game, bluff=0):
    # Same bot as above but tries to guess the dice of other players.

    # First we guess the expectations without any knowledge of the dice
    default_exp = [(2 - index // 6) / 6 * (np.sum(game.dice_nr)) for index in range(1, 7)]

    # Now if a player makes a guess that is above the defaul approximation we guess that he has one more than expected this die.
    dice_guess = [[0]*len(game.players) for _ in range(6)]
    for h in game.history[::-1]:
        h_state = h[1]
        if h_state[0]>default_exp[h_state[1]-1]:
            dice_guess[h_state[1]-1][h[0]]=1+1/6*game.dice_nr[h[0]]# + dice_guess[h[0]]*.1

    my_exp = [game.get_my_dice().count(i)
              + game.get_my_dice().count(6)
              + sum(dice_guess[i - 1]) * 2 / 6
              + (2 - i // 6) / 6 * ((np.sum(game.dice_nr)) - len(game.get_my_dice()) - len(dice_guess))
              for i in range(1, 7)]

    return _get_move_from_expectationis(game, my_exp, bluff)
