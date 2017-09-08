import nn

# init
_nn = nn.NeuralNetwork(2, 1, 3, 1)
_test = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
_nn.setEA(.5, .7)

# leaning
for epoch in range(1000):
    for params in _test:
        _nn.set([params[0], params[1]])

        _nn.learning([params[2]])

        r = _nn.result()
        mse = _nn.mse(r, [params[2]])

        r = r[0]
        mse = mse[0]

        print('Error: ', round(mse * 100, 2))

# e2e
for params in _test:
    _nn.set([params[0], params[1]])

    r = _nn.result()
    mse = _nn.mse(r, [params[2]])

    r = r[0]
    mse = mse[0]

    print('E2E: r =', round(r), '-', params[2], r, round(mse * 100, 2), '%')