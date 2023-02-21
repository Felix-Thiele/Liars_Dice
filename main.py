import bluff
import bots
import train_ai_bot

# ai experiments not working yet
#train_ai_bot.train()

agent_dict = {'human_agent':bots.human_move,
    'random':bots.random_bot,
    'ai_trained_like_rem': train_ai_bot.ai_agent,
    'best_exp': bots.bot_best_expectation,
    'best_exp_remember_hist': bots. bot_best_expectation_with_hist,
    'best_exp_bluff_1': lambda g: bots.bot_best_expectation(g, bluff=1),
    'best_exp_remember_hist_bluff_1': lambda g: bots.bot_best_expectation_with_hist(g, bluff=1),
    'best_exp_remember_hist_bluff_2': lambda g: bots.bot_best_expectation_with_hist(g, bluff=2)}


agents = ['random', 'best_exp',
#          'ai_trained_like_rem',
          'best_exp_remember_hist',
          'best_exp_bluff_1',
          'best_exp_remember_hist_bluff_1',
          'best_exp_remember_hist_bluff_2']
winners = []
g = bluff.bluff_gamestate([agent_dict[b] for b in agents])
for i in range(300):
    g.reset()
    result = g.play_game(True)
    winners.append(result)
for i in set(winners):
    print(' won ', winners.count(i), ' times with: bot ', agents[i])
