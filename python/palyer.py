import nn

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

__nn.save('t.b')
__nn.load('t.b')