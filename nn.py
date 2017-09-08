import math
import random
from enum import Enum

class Connect:

    def __init__(self, base, way):
        # self.weight = random.uniform(-1, 1)
        self.weight = random.random()
        self.base = base
        self.way = way
        self.name = ''
        self.deltaWeight = 0

    def echo(self):
        return self.way.power * self.weight

    def learning(self, E, A):
        gradWeight = self.base.delta * self.way.power
        self.deltaWeight = (E * gradWeight) + (A * self.deltaWeight)
        self.weight = self.weight + self.deltaWeight


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
        self.name = ''

    def addConnect(self, to):
        self.connects.append(to)

    def addBack(self, to):
        self.backs.append(to)

    def setInput(self, value):
        self.input = value

    def learning(self, E, A):
        for connect in self.connects:
            connect.learning(E, A)

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

    def learning(self, E, A):
        for neuron in self.neurons:
            neuron.learning(E, A)

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

    def learning(self, E, A):
        self.calc()
        for layout in self.layouts:
            layout.learning(E, A)

    def calcDelta(self):
        self.calc()
        for layout in self.layouts:
            for neuron in layout.neurons:
                delta = .0
                for neuronBack in neuron.backs:
                    weight = .0
                    for connect in neuronBack.connects:
                        if connect.way == neuron:
                            weight = connect.weight
                            break

                    delta += neuronBack.delta * weight
                neuron.delta = ((1 - neuron.power) * neuron.power) * delta
                

    def calc(self):
        for layout in self.layouts:
            layout.process()


class InputLayout:

    def __init__(self, size, hiddenLayout):
        self.size = size
        if self.size > 0:
            self.layout = Layout(self.size, NeuronType.INPUT)
            hiddenLayout.layouts[0].bind(self.layout)

    def set(self, number, value):
        if number > self.size:
            pass  # error

        self.layout.neurons[number].power = value

    def learning(self, E, A):
        self.layout.learning(E, A)


class ResultLayout:

    def __init__(self, size, hiddenLayout):
        self.size = size
        self.hidden = hiddenLayout
        if self.size > 0:
            self.layout = Layout(self.size, NeuronType.OUTPUT)
            self.layout.bind(self.hidden.layouts[self.hidden.depth - 1])

    def result(self):
        r = []
        self.layout.process()

        for neuron in self.layout.neurons:
            r.append(neuron.power)

        return r

    def learning(self, correct, E, A):
        if len(correct) > self.size:
            pass  # error

        self.layout.process()

        for x in range(len(correct)):
            neuron = self.layout.neurons[x]
            neuron.delta = (correct[x] - neuron.power) * \
                ((1 - neuron.power) * neuron.power)

        self.hidden.calcDelta()

        for neuron in self.layout.neurons:
            neuron.learning(E, A)


class NeuralNetwork:

    def __init__(self, sizeInput, sizeOutput, sizeHidden, depthHidden):
        self.hidden = HiddenLayout(sizeHidden, depthHidden)
        self.input = InputLayout(sizeInput, self.hidden)
        self.output = ResultLayout(sizeOutput, self.hidden)

        self.E = 0.7
        self.A = 0.3

    def set(self, params):
        if len(params) > self.input.size:
            pass  # error

        for x in range(len(params)):
            self.input.set(x, params[x])

    def result(self):
        self.hidden.calc()
        return self.output.result()

    def mse(self, result, correct):
        mse = []

        if len(result) != len(correct):
            return mse # error

        for x in range(len(result)):
            mse.append(pow(correct[x] - result[x], 2) / 1)

        return mse
    
    def setEA(self, E, A):
        self.E = E
        self.A = A

    def learning(self, correct):
        if len(correct) > self.output.size:
            pass  # error

        self.hidden.calc()
        self.output.learning(correct, self.E, self.A)
        self.hidden.learning(self.E, self.A)
        self.input.learning(self.E, self.A)