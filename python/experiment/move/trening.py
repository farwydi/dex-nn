import os
import random

import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

model = Sequential()
input = Dense(18, input_shape=(5,), activation="relu")
model.add(input)
hidden_1 = Dense(32, activation="tanh")
model.add(hidden_1)
model.add(Dropout(0.35))
hidden_2 = Dense(32, activation="tanh")
model.add(hidden_2)
model.add(Dropout(0.35))
output = Dense(4, activation="sigmoid")
model.add(output)

model.compile(loss="mean_squared_error",
              optimizer="Adam")

#  environment
#  0 - well, 1 - poison, 2 - food, 3 - thought, 4 - health
#  0 - move, 1 - rotate, 2 - eat, 3 - fix

COUNT_DATASET = 100000
DATASET = np.zeros((COUNT_DATASET, 4), dtype='float32')
REPLY = np.zeros((COUNT_DATASET, 5), dtype='float32')
for itr in range(COUNT_DATASET):
    well = random.randint(0, 1)
    poison = random.randint(0, 1)
    food = random.randint(0, 1)
    thought = random.random()
    health = random.random()

    data_set = [1, 0, 0, 0]

    if well == 1:
        data_set[1] = random.random()
    else:
        if poison == 1:
            data_set[3] = 1
        else:
            if food == 1:
                data_set[2] = 1

    DATASET[itr] = tuple(data_set)
    REPLY[itr] = (well, poison, food, thought, health)

# data = np.array([(0, 0, 0, 1, 1), (1, 0, 0), (0, 1, 0), (0, 0, 1)])
# out = np.array([(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)])

model.fit(REPLY, DATASET, epochs=10)

print('Res: ', model.evaluate(REPLY, DATASET, verbose=0))

model_json = model.to_json()
json_file = open("moveGame.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("moveGame.h5")
