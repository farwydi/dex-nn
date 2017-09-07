import nn

# init
_nn = nn.NeuralNetwork(2, 1, 3, 1)
_test = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

# leaning
for epoch in range(10):
    for params in _test:
        _nn.set([params[0], params[1]])
        _nn.learning([params[2]])

# e2e
for params in _test:
    _nn.set([params[0], params[1]])

    r = _nn.result()
    mse = _nn.mse(r)

    print('E2E: r =', round(r[0]), '-', params[2], r[0], mse[0] * 100)