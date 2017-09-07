import math
import random
from enum import Enum


class Connect:

    def __init__(self, A, B):
        # self.weight = random.uniform(-1, 1)
        self.weight = random.random()
        self.aNeuron = A
        self.bNeuron = B
        self.deltaW_i = 0
        self.E = 0.7
        self.Α = 0.3

    def echo(self):
        return self.bNeuron.power * self.weight

    def learning(self):
        gradWeight = self.aNeuron.delta * self.aNeuron.power
        self.deltaW_i = (self.E * gradWeight) + (self.Α * self.deltaW_i)
        self.weight = self.weight + self.deltaW_i


class NeuronType(Enum):
    INPUT = 0
    OUTPUT = 1
    HIDDEN = 2


class Neuron:

    def __init__(self, type):
        self.connects = []
        self.power = .0
        self.delta = .0
        self.backs = []
        self.type = type

    def addConnect(self, to):
        self.connects.append(to)

    def addBack(self, to):
        self.backs.append(to)

    def setInput(self, value):
        self.input = value

    def learning(self):
        for connect in self.connects:
            connect.learning()

    def sum(self):
        r = .0
        for connect in self.connects:
            r += connect.echo()

        return r


class Layout:

    def __init__(self, size, type):
        self.neurons = []

        for nSize in range(size):
            neuron = Neuron(type)
            self.neurons.append(neuron)

    def bind(self, layout):
        for host in self.neurons:
            for guest in layout.neurons:
                connect = Connect(host, guest)
                host.addConnect(connect)
                guest.addBack(host)

    def f(self, x):
        return 1 / (1 + pow(math.e, -1 * x))
        # return (pow(math.e, 2 * x) - 1) / (pow(math.e, 2 * x) + 1)

    def process(self):
        for neuron in self.neurons:
            s = neuron.sum()
            neuron.power = self.f(s)

    def learning(self):
        for neuron in self.neurons:
            delta = .0
            for neuronBack in neuron.backs:
                weight = .0
                for connect in neuronBack.connects:
                    if connect.bNeuron == neuron:
                        weight = connect.weight
                        break

                delta += neuronBack.delta * weight
            neuron.delta = ((1 - neuron.power) * neuron.power) * delta
            neuron.learning()


class HiddenLayout:

    def __init__(self, size=10, depth=2):
        self.layouts = []
        self.size = size
        self.depth = depth

        for nDepth in range(depth):
            layout = Layout(size, NeuronType.HIDDEN)
            self.layouts.append(layout)

            if nDepth > 0:
                self.layouts[nDepth - 1].bind(self.layouts[nDepth])

    def learning(self):
        self.calc()
        for layout in self.layouts:
            layout.learning()

    def calc(self):
        for layout in self.layouts:
            layout.process()


class InputLayout:

    def __init__(self, size, hiddenLayout):
        self.size = size
        self.layout = Layout(self.size, NeuronType.INPUT)
        hiddenLayout.layouts[0].bind(self.layout)

    def set(self, number, value):
        if number > self.size:
            pass  # error

        self.layout.neurons[number].power = value

    def learning(self):
        self.layout.learning()


class ResultLayout:

    def __init__(self, size, hiddenLayout):
        self.size = size
        self.layout = Layout(self.size, NeuronType.OUTPUT)
        self.hidden = hiddenLayout
        self.layout.bind(self.hidden.layouts[self.hidden.depth - 1])

    def result(self):
        r = []
        self.layout.process()

        for neuron in self.layout.neurons:
            r.append(neuron.power)

        return r

    def learning(self, correct):
        if len(correct) > self.size:
            pass  # error

        self.layout.process()

        for x in range(len(correct)):
            neuron = self.layout.neurons[x]
            neuron.delta = (correct[x] - neuron.power) * \
                ((1 - neuron.power) * neuron.power)
            neuron.learning()


class NeuralNetwork:

    def __init__(self, sizeInput, sizeOutput, sizeHidden, depthHidden):
        self.hidden = HiddenLayout(sizeHidden, depthHidden)
        self.input = InputLayout(sizeInput, self.hidden)
        self.output = ResultLayout(sizeOutput, self.hidden)

    def set(self, params):
        if len(params) > self.input.size:
            pass  # error

        for x in range(len(params)):
            self.input.set(x, params[x])

    def result(self):
        self.hidden.calc()
        return self.output.result()

    def mse(self, result):
        mse = []
        for r in result:
            mse.append(pow(1 - r, 2) / 1)

        return mse

    def learning(self, correct):
        if len(correct) > self.output.size:
            pass  # error

        self.hidden.calc()
        self.output.learning(correct)
        self.hidden.learning()
        self.input.learning()

# init
_nn = NeuralNetwork(2, 1, 3, 1)
_test = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

# leaning
for epoch in range(1):
    for params in _test:
        _nn.set([params[0], params[1]])
        _nn.learning([params[2]])

# e2e
for params in _test:
    _nn.set([params[0], params[1]])

    r = _nn.result()
    mse = _nn.mse(r)

    print('E2E: r =', round(r[0]), '-', params[2], r[0], mse[0] * 100)


import numpy

# import matplotlib.pyplot as plt

# fig = plt.figure()
# # Добавление на рисунок прямоугольной (по умолчанию) области рисования
# scatter1 = plt.scatter(0.0, 1.0)
# print('Scatter: ', type(scatter1))

# graph1 = plt.plot([-1.0, 1.0], [0.0, 1.0])
# print('Plot: ', len(graph1), graph1)

# text1 = plt.text(0.5, 0.5, 'Text on figure')
# print('Text: ', type(text1))

# grid1 = plt.grid(True)   # линии вспомогательной сетки

# plt.show()