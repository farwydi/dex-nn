import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

model = Sequential()

model.add(Dense(3, input_dim=2, activation="tanh"))
model.add(Dense(1, activation="sigmoid"))

sgd = SGD(lr=.15)
model.compile(loss="binary_crossentropy",
              optimizer=sgd)

# print(model.summary())

data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
labels = np.array([[0], [1], [1], [0]])


model.fit(data, labels, batch_size=1, epochs=2500, verbose=1)

print(model.predict_proba(data))

model_json = model.to_json()
json_file = open("xor.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("xor.h5")

# score = model.evaluate(data, labels)
# print("Score: ", score * 100)
