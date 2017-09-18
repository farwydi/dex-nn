from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

import numpy as np

model = Sequential()
model.add(Dense(6, input_shape=(2,), activation='tanh'))
# model.add(Dropout(.2))
model.add(Dense(2, activation='tanh'))


model.compile(loss="mean_squared_error",
              optimizer="Adam")

data = np.array([(0, 0), (0, 1), (1, 0), (1, 1)])
out = np.array([(1), (1, -1), (-1, 1), (-1, -1)])

model.fit(data, out, epochs=1500)

print('Res: ', model.evaluate(data, out, verbose=0))

model_json = model.to_json()
json_file = open("move.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("move.h5")