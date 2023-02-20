import bluff
import bots

agent_dict = {'human_agent':bots.human_move,
    'best_exp': bots.bot_best_expectation,
    'best_exp_remember_hist': bots. bot_best_expectation_with_hist,
    'best_exp_bluff_1': lambda g: bots.bot_best_expectation(g, bluff=1),
    'best_exp_remember_hist_bluff_1': lambda g: bots.bot_best_expectation_with_hist(g, bluff=1),
    'best_exp_remember_hist_bluff_2': lambda g: bots.bot_best_expectation_with_hist(g, bluff=2)}


agents = ['human_agent', 'best_exp', 'best_exp_remember_hist', 'best_exp_bluff_1', 'best_exp_remember_hist_bluff_1', 'best_exp_remember_hist_bluff_2']
winners = []
for i in range(1):
    g = bluff.bluff_gamestate([agent_dict[b] for b in agents])
    winners.append(g.play_game())
for i in set(winners):
    print(' won ', winners.count(i), ' times with: bot ', agents[i])
