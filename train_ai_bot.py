import bluff
import numpy as np
import tensorflow as tf
import random
from tqdm import tqdm
import bots


#### MEH doesnt work yet


def get_model():
        inputs = tf.keras.Input(shape=(148,))
        x = tf.keras.layers.Dense(150, activation=tf.nn.relu)(inputs)
        x = tf.keras.layers.Dense(150, activation=tf.nn.relu)(x)
        x = tf.keras.layers.Dense(150, activation=tf.nn.relu)(x)
        x = tf.keras.layers.Dense(50, activation=tf.nn.relu)(x)
        outputs = tf.keras.layers.Dense(1, activation=tf.math.tanh)(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)

        model.compile(
            loss=tf.keras.losses.MeanAbsoluteError(),
            optimizer=tf.keras.optimizers.Adam(),
        )

        return model

def model_agent(game, model):

    state = game.get_encoding()
    last_non_zero = max(37, np.max(np.nonzero(state)))
    possible_states = []
    next_moves = list(range(last_non_zero + 1, min(len(state), last_non_zero + 13, 146))) + [147]
    for i in next_moves:
        state[i] = 1
        possible_states.append(state.copy())
        state[i] = 0
    next_move_values = model.predict(np.array(possible_states), verbose=0).reshape(-1)
    #print(next_move_values)
    next_move_values = np.array(next_move_values)
    if np.all(next_move_values<=0):
        return game.list_possible_states[next_moves[np.argmax(next_move_values)]-36]
    else:
        next_move_values = next_move_values[next_move_values>0]
        probability = next_move_values/np.sum(next_move_values)
        result = np.random.choice([i for i in range(len(next_move_values))], 1, p=probability)[0]
        return game.list_possible_states[next_moves[result]-36]


def train(self_play_batches=3, self_play_batchsize=300):

    def noise(y, sig=.5):
        y = y+np.random.normal(0, sig)
        y[y>1]=1
        y[y<-1]=-1
        return y

    model = get_model()

    # pretrain with hardcoded bot
    for _ in range(20):
        g = bluff.bluff_gamestate([random.choice([lambda g: bots.bot_best_expectation_with_hist(g, bluff=0), lambda g: bots.bot_best_expectation_with_hist(g, bluff=0), lambda g: bots.bot_best_expectation(g, bluff=20)]) for _ in range(2,9)])
        x_train, y_train = g.collect_data(1000)
        # print(np.count_nonzero(y_train==0)/np.count_nonzero(y_train==1))
        model.fit(x_train, noise(y_train, random.uniform(0.2, 0.6)), batch_size=64, epochs=5, validation_split=0.2)

    # train against itself
    for _ in tqdm(range(self_play_batches)):
        g = bluff.bluff_gamestate([lambda game: model_agent(game, model)]*random.randint(2, 4))
        x_train,y_train = g.collect_data(self_play_batchsize)
        model.fit(x_train, noise(y_train, random.uniform(0.3, 0.4)), batch_size=64, epochs=5, validation_split=0.2)


    model.save('ai_half_self_trained')


