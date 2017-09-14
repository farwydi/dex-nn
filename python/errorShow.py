import matplotlib.pyplot as plt
import numpy as np
import nn

_nn = nn.NeuralNetwork(2, 1, 5, 1)
_test = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
_nn.setEA(.15, .3)

rr = []

# leaning
for epoch in range(10000):
    msesum = .0
    for params in _test:
        _nn.set([params[0], params[1]])

        _nn.learning([params[2]])

        msesum += round(_nn.mse(_nn.result(), [params[2]])[0] * 100, 2)

    rr.append(msesum / 4)

plt.plot(rr)

plt.ylabel('error')
plt.xlabel('t (learning time)')

plt.grid(True)


plt.show()