from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy as np

model = Sequential()
l1 = LSTM(32, input_shape=(10, 64))
model.add(l1)

print(l1.get_weights())