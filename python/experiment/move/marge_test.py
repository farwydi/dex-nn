import random

import numpy as np

# from keras.layers import Dense, Dropout
# from keras.models import Sequential


def random_gen(size, max_value):
    gen = []
    for _ in range(size):
        rand_gen = round(random.uniform(0, max_value - 1))
        try:
            gen.index(rand_gen)
        except ValueError:
            gen.append(rand_gen)

    return gen


def merge_liner(size, weights_1, weights_2, mutation):
    replace = round(size / 2)
    gen = random_gen(replace, size)
    result = np.zeros(size, dtype='float32')

    for itr in gen:
        result[itr] = weights_1[itr]

    for itr, _ in np.ndenumerate(weights_2):
        itr = itr[0]
        if itr not in gen:
            result[itr] = weights_2[itr]

    if mutation:
        replace = round(size * 0.2)
        gen = random_gen(replace, size)
        for itr in gen:
            result[itr] = random.uniform(-1, 1)

    return result


def merge(weights_1, weights_2, mutation=True):
    '''
    merge xx algorithm
    Merge half
    Mutation default 20%

    # param
    weights_1 = [[ [weight], [weight], [weight] ], [offsets]]
    '''
    if len(weights_1[0]) != len(weights_2[0]):
        raise Exception()

    if len(weights_1[0][0]) != len(weights_2[0][0]):
        raise Exception()

    if len(weights_1[1]) != len(weights_2[1]):
        raise Exception()

    depth_weights = len(weights_1[0])
    size_weights = len(weights_1[0][0])

    result = [np.zeros((depth_weights, size_weights), dtype='float32'), np.zeros(
        size_weights, dtype='float32')]

    for depth in range(depth_weights):
        result[0][depth] = merge_liner(
            size_weights, weights_1[0][depth], weights_2[0][depth], mutation)

    return result

# model = Sequential()

# input = Dense(18, input_shape=(6,), activation="relu")
# hidden_1 = Dense(32, activation="softmax")
# hidden_2 = Dense(32, activation="softmax")
# output = Dense(4, activation="linear")

# model.add(input)
# model.add(hidden_1)
# model.add(Dropout(0.35))
# model.add(hidden_2)
# model.add(Dropout(0.35))
# model.add(output)

# print(input.get_weights())


W__1 = [np.random.randn(6, 18), np.zeros(18)]
W__2 = [np.random.randn(6, 18), np.zeros(18)]

WW = merge(W__1, W__2)
print(WW)

# w1 = np.asarray([], dtype='float32')
