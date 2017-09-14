import nn

# init
_nn = nn.NeuralNetwork(2, 1, 3, 1)
_test = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
_nn.setEA(.15, .3)

# leaning
for epoch in range(80000):
    for params in _test:
        _nn.set([params[0], params[1]])

        _nn.learning([params[2]])

        r = _nn.result()
        mse = _nn.mse(r, [params[2]])
        mse = mse[0]

        print('Error: ', round(mse * 100, 2))

# e2e
_nn.save('xor.nn')