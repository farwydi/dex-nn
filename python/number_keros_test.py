import numpy

from keras.models import Sequential, model_from_json
from keras.datasets import mnist

json_model = open("mnist_model.json", "r")
json_model_data = json_model.read()
json_model.close()

model = model_from_json(json_model_data)
model.load_weights("mnist_model.h5")

(x_train, y_train), (x_test, y_test) = mnist.load_data()

model.compile(loss="categorical_crossentropy",
              optimizer="SGD", metrics=["accuracy"])

score = model.evaluate(x_train, y_test, verbose=0)
print("Score: %.2f%%" % (score[1] * 100))
