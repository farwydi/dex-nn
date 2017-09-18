import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from keras.models import Sequential, model_from_json
from keras.optimizers import SGD

json_model = open("xor.json", "r")
json_model_data = json_model.read()
json_model.close()

model = model_from_json(json_model_data)
model.load_weights("xor.h5")

data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
labels = np.array([[0], [1], [1], [0]])

sgd = SGD(lr=.15)
model.compile(loss="binary_crossentropy",
              optimizer=sgd)

score = model.evaluate(data, labels)
print("Score: ", score * 100)

from keras.utils import plot_model
plot_model(model, show_shapes=True)