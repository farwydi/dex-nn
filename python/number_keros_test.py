import numpy

from keras.models import Sequential, model_from_json
from keras.datasets import mnist
from keras.utils import np_utils

json_model = open("mnist_model.json", "r")
json_model_data = json_model.read()
json_model.close()

model = model_from_json(json_model_data)
model.load_weights("mnist_model.h5")

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_train = x_train.astype('float32')
x_train /= 255

x_train = np_utils.to_categorical(x_train, 10)

model.compile(loss="categorical_crossentropy",
              optimizer="SGD", metrics=["accuracy"])

score = model.evaluate(x_train, x_train)
print("Score: %.2f%%" % (score * 100))
