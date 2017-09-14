import numpy

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

numpy.random.seed(45)

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_train = x_train.astype('float32')
x_train /= 255

y_train = np_utils.to_categorical(y_train, 10)

model = Sequential()

model.add(Dense(800, input_dim=784, kernel_initializer="normal", activation="relu"))
model.add(Dense(10, kernel_initializer="normal", activation="softmax"))

model.compile(loss="categorical_crossentropy",
              optimizer="SGD", metrics=["accuracy"])

print(model.summary())

model.fit(x_train, y_train, validation_split=0.2, batch_size=200, epochs=100, verbose=1)

model_json = model.to_json()
json_file = open("mnist_model.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("mnist_model.h5")