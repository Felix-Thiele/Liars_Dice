import bluff
import numpy as np
import tensorflow as tf
import random
from tqdm import tqdm
import bots

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
    for i in list(range(last_non_zero + 1, min(len(state), last_non_zero + 20))) + [-1]:
        state[i] = 1
        possible_states.append(state.copy())
        state[i] = 0
    next_move_values = model.predict(np.array(possible_states), verbose=0)
    next_move_values = np.array(next_move_values)
    if np.all(next_move_values<=0):
        return game.list_possible_states[last_non_zero-37 + np.argmax(next_move_values)+2]
    else:
        next_move_values = next_move_values[next_move_values>0]
        probability = next_move_values/np.sum(next_move_values)
        result = np.random.choice([i for i in range(len(next_move_values))], 1, p=probability)[0]
        return game.list_possible_states[last_non_zero-37+result+2]


def train(self_play_batches=10, self_play_batchsize=100):

    model = get_model()

    # pretrain with hardcoded bot
    for _ in range(5):
        g = bluff.bluff_gamestate([lambda g: bots.bot_best_expectation_with_hist(g, bluff=2)] * random.randint(2, 5))
        x_train, y_train = g.collect_data(100000)
        model.fit(x_train, y_train, batch_size=64, epochs=100, validation_split=0.2)

    for _ in tqdm(range(self_play_batches)):
        g = bluff.bluff_gamestate([lambda game: model_agent(game, model)]*random.randint(2, 5))
        x_train,y_train = g.collect_data(self_play_batchsize)
        model.fit(x_train, y_train, batch_size=64, epochs=2, validation_split=0.2)


train()
