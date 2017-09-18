from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

import numpy as np

model = Sequential()
model.add(Dense(18, input_shape=(3,), activation='relu'))
# model.add(Dropout(.2))
model.add(Dense(4, activation='linear'))


model.compile(loss="mean_squared_error",
              optimizer="Adam")

data = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)])
out = np.array([(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)])

model.fit(data, out, epochs=300)

print('Res: ', model.evaluate(data, out, verbose=0))

model_json = model.to_json()
json_file = open("moveGame.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("moveGame.h5")