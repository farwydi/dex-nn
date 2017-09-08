import unittest
import nn

class TestNeuralNetwork(unittest.TestCase):

    def test_learning(self):
        __nn = nn.NeuralNetwork(2, 1, 2, 1)
        __nn.set([1, 0])

        __nn.result()

        self.assertEqual(round(__nn.output.layout.neurons[0].power), 1)

    def test_soft_learning(self):
        __nn = nn.NeuralNetwork(2, 1, 2, 1)
        __nn.set([1, 0])

        __nn.input.layout.neurons[0].name = 'I1'
        __nn.input.layout.neurons[1].name = 'I2'

        # h1 w1
        __nn.hidden.layouts[0].neurons[0].name = 'H1'
        __nn.hidden.layouts[0].neurons[0].connects[0].weight = 0.45
        __nn.hidden.layouts[0].neurons[0].connects[0].name = 'w1'
        # h1 w3
        __nn.hidden.layouts[0].neurons[0].connects[1].weight = -0.12
        __nn.hidden.layouts[0].neurons[0].connects[1].name = 'w3'
        # h2 w2
        __nn.hidden.layouts[0].neurons[1].name = 'H2'
        __nn.hidden.layouts[0].neurons[1].connects[0].weight = 0.78
        __nn.hidden.layouts[0].neurons[1].connects[0].name = 'w2'
        # h2 w4
        __nn.hidden.layouts[0].neurons[1].connects[1].weight = 0.13
        __nn.hidden.layouts[0].neurons[1].connects[1].name = 'w4'

        __nn.output.layout.neurons[0].name = 'O1'
        __nn.output.layout.neurons[0].connects[0].weight = 1.5
        __nn.output.layout.neurons[0].connects[0].name = 'w5'
        __nn.output.layout.neurons[0].connects[1].weight = -2.3
        __nn.output.layout.neurons[0].connects[1].name = 'w6'

        __nn.learning([1])
        __nn.result()

        self.assertEqual(round(__nn.output.layout.neurons[0].power, 2), 0.37)

    def test_soft(self):
        __nn = nn.NeuralNetwork(2, 1, 2, 1)
        __nn.set([1, 0])

        __nn.input.layout.neurons[0].name = 'I1'
        __nn.input.layout.neurons[1].name = 'I2'

        # h1 w1
        __nn.hidden.layouts[0].neurons[0].name = 'H1'
        __nn.hidden.layouts[0].neurons[0].connects[0].weight = 0.45
        __nn.hidden.layouts[0].neurons[0].connects[0].name = 'w1'
        # h1 w3
        __nn.hidden.layouts[0].neurons[0].connects[1].weight = -0.12
        __nn.hidden.layouts[0].neurons[0].connects[1].name = 'w3'
        # h2 w2
        __nn.hidden.layouts[0].neurons[1].name = 'H2'
        __nn.hidden.layouts[0].neurons[1].connects[0].weight = 0.78
        __nn.hidden.layouts[0].neurons[1].connects[0].name = 'w2'
        # h2 w4
        __nn.hidden.layouts[0].neurons[1].connects[1].weight = 0.13
        __nn.hidden.layouts[0].neurons[1].connects[1].name = 'w4'

        __nn.output.layout.neurons[0].name = 'O1'
        __nn.output.layout.neurons[0].connects[0].weight = 1.5
        __nn.output.layout.neurons[0].connects[0].name = 'w5'
        __nn.output.layout.neurons[0].connects[1].weight = -2.3
        __nn.output.layout.neurons[0].connects[1].name = 'w6'

        __nn.result()

        self.assertEqual(round(__nn.output.layout.neurons[0].power, 2), 0.34)

    def test_force(self):
        i1 = nn.Neuron(nn.NeuronType.INPUT)
        i1.power = 1
        i1.name = 'INPUT 1'
        i2 = nn.Neuron(nn.NeuronType.INPUT)
        i2.power = 0
        i2.name = 'INPUT 2'

        h1 = nn.Neuron(nn.NeuronType.HIDDEN)
        h1.name = 'HIDDEN 1'
        h2 = nn.Neuron(nn.NeuronType.HIDDEN)
        h2.name = 'HIDDEN 2'

        op = nn.Neuron(nn.NeuronType.OUTPUT)
        op.name = 'OUTPUT'

        h1.addBack(op)
        h2.addBack(op)

        i1.addBack(h1)
        i1.addBack(h2)

        i2.addBack(h1)
        i2.addBack(h2)

        w1 = nn.Connect(h1, i1)
        w1.weight = .45
        w2 = nn.Connect(h2, i1)
        w2.weight = .78

        w3 = nn.Connect(h1, i2)
        w3.weight = -0.12
        w4 = nn.Connect(h2, i2)
        w4.weight = .13

        h1.addConnect(w1)
        h1.addConnect(w3)
        h2.addConnect(w2)
        h2.addConnect(w4)

        w5 = nn.Connect(op, h1)
        w5.weight = 1.5
        w6 = nn.Connect(op, h2)
        w6.weight = -2.3

        op.addConnect(w5)
        op.addConnect(w6)

        __nn = nn.NeuralNetwork(2, 1, 2, 1)

        __nn.input.layout = nn.Layout(0, nn.NeuronType.INPUT)
        __nn.input.layout.neurons.append(i1)
        __nn.input.layout.neurons.append(i2)

        __nn.output.layout = nn.Layout(0, nn.NeuronType.OUTPUT)
        __nn.output.layout.neurons.append(op)

        __nn.hidden.layouts = []
        hl_l1 = nn.Layout(0, nn.NeuronType.HIDDEN)
        hl_l1.neurons.append(h1)
        hl_l1.neurons.append(h2)
        __nn.hidden.layouts.append(hl_l1)

        __nn.result()
        self.assertEqual(round(op.power, 2), 0.34)

        # __nn.learning([1])
        # __nn.result()

        # self.assertEqual(round(w1.weight, 1), 0.5)
        # self.assertEqual(round(w2.weight, 2), 0.73)
        # self.assertEqual(round(w3.weight, 2), -0,12)
        # self.assertEqual(round(w4.weight, 2), 0.13)
        # self.assertEqual(round(w5.weight, 3), 1.563)
        # self.assertEqual(round(w6.weight, 2), -2.2)
        # self.assertEqual(round(op.power, 2), 0.37)

unittest.main()