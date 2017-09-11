#include "nn.h"
#include "neuron.h"
#include "connect.h"

NeuralNetwork::NeuralNetwork()
{
    for (size_t i = 0; i < HIDDEN_DEPTH; i++) {
        for (size_t n = 0; n < HIDDEN_SIZE; n++) {
            hidden[i][n] = new Neuron(NeuronType::HIDDEN, ((i == 0) ? INPUT_SIZE : HIDDEN_SIZE),
                                      ((i == HIDDEN_DEPTH) ? OUTPUT_SIZE : HIDDEN_SIZE), n,
                                      "HIDDEN_" + to_string(i));
        }
    }

    for (size_t n = 0; n < INPUT_SIZE; n++) {
        input[n] = new Neuron(NeuronType::INPUT, 0, HIDDEN_SIZE, n, "INPUT");
    }

    for (size_t n = 0; n < OUTPUT_SIZE; n++) {
        output[n] = new Neuron(NeuronType::OUTPUT, HIDDEN_SIZE, 0, n, "OUTPUT");
    }

    for (auto hiddenNeuron : hidden[0]) {
        for (auto inputNeuron : input) {
            hiddenNeuron->addConnect(new Connect(hiddenNeuron, inputNeuron));
            inputNeuron->addBack(hiddenNeuron);
        }
    }

#if HIDDEN_DEPTH > 1
    size_t offset = 1;
    auto tail = hidden[offset];
    while (true) {
        auto front = hidden[offset - 1];

        for (auto tailNeuron : tail) {
            for (auto frontNeuron : front) {
                tailNeuron->addConnect(new Connect(tailNeuron, frontNeuron));
                frontNeuron->addBack(tailNeuron);
            }
        }

        offset += 1;

        if (offset >= HIDDEN_DEPTH) {
            break;
        }
    }
#endif

    for (auto outputNeuron : output) {
        for (auto hiddenNeuron : hidden[HIDDEN_DEPTH - 1]) {
            outputNeuron->addConnect(new Connect(outputNeuron, hiddenNeuron));
            hiddenNeuron->addBack(outputNeuron);
        }
    }
}

NeuralNetwork::~NeuralNetwork() {}

void NeuralNetwork::set(array<float, INPUT_SIZE> params)
{
    for (size_t i = 0; i < INPUT_SIZE; i++) {
        input[i]->setPower(params[i]);
    }
}

array<float, OUTPUT_SIZE> NeuralNetwork::result(bool _calc)
{
    array<float, OUTPUT_SIZE> result;

    if (_calc) {
        calc();
    }

    for (size_t i = 0; i < OUTPUT_SIZE; i++) {
        result[i] = output[i]->getPower();
    }

    return result;
}

void NeuralNetwork::save(string name)
{
    ofstream f(name, ofstream::binary);

    f.write(reinterpret_cast<const char *>(&HIDDEN_DEPTH), 4);
    f.write(reinterpret_cast<const char *>(&HIDDEN_SIZE), 4);
    f.write(reinterpret_cast<const char *>(&INPUT_SIZE), 4);
    f.write(reinterpret_cast<const char *>(&OUTPUT_SIZE), 4);

    for (auto neuron : output) {
        auto weights = neuron->getWeights();
        f.write(reinterpret_cast<const char *>(&weights.size()), 4);
        f.write(reinterpret_cast<const char *>(weights.data()), weights.size());
    }

    for (auto depth : hidden) {
        for (auto neuron : depth) {
            auto weights = neuron->getWeights();
            f.write(reinterpret_cast<const char *>(&weights.size()), 4);
            f.write(reinterpret_cast<const char *>(weights.data()), weights.size());
        }
    }

    f.close();
}

void NeuralNetwork::load(string name)
{
    ifstream f(name, ifstream::binary);

    int hiddenDepth;
    f.read(reinterpret_cast<char *>(&hiddenDepth), 4);

    int hiddenSize;
    f.read(reinterpret_cast<char *>(&hiddenSize), 4);

    int inputSize;
    f.read(reinterpret_cast<char *>(&inputSize), 4);

    int outputSize;
    f.read(reinterpret_cast<char *>(&outputSize), 4);

    for (int i = 0; i < outputSize; i++) {
        unsigned int size;
        f.read(reinterpret_cast<char *>(&size), 4);

        vector<NN_POINT> weights(size);
        f.read(reinterpret_cast<char *>(weights.data()), size);

        output[i]->restore(weights);
    }

    f.close();
}

array<float, OUTPUT_SIZE> NeuralNetwork::mse(array<float, OUTPUT_SIZE> result,
                                             array<float, OUTPUT_SIZE> correct)
{
    array<float, OUTPUT_SIZE> mse;

    for (size_t n = 0; n < OUTPUT_SIZE; n++) {
        mse[n] = pow(correct[n] - result[n], 2) / 1;
    }

    return mse;
}

array<float, OUTPUT_SIZE> NeuralNetwork::learning(array<float, OUTPUT_SIZE> correct)
{
    calc();

    for (int n = 0; n < OUTPUT_SIZE; n++) {
        output[n]->setDelta((correct[n] - output[n]->getPower()) *
                            ((1 - output[n]->getPower()) * output[n]->getPower()));
    }

    for (int i = HIDDEN_DEPTH - 1; i >= 0; i--) {
        for (int n = 0; n < HIDDEN_SIZE; n++) {
            NN_POINT potential = hidden[i][n]->getBackPotential();

            hidden[i][n]->setDelta(((1 - hidden[i][n]->getPower()) * hidden[i][n]->getPower()) *
                                   potential);
        }
    }

    for (auto neuron : output) {
        neuron->learning();
    }

    for (auto depth : hidden) {
        for (auto neuron : depth) {
            neuron->learning();
        }
    }

    for (auto neuron : input) {
        neuron->learning();
    }

    return result();
}

NN_POINT NeuralNetwork::normalize(NN_POINT x)
{
    return 1 / (1 + exp(-1 * x));
}

void NeuralNetwork::calc()
{
    for (auto depth : hidden) {
        for (auto neuron : depth) {
            neuron->setPower(normalize(neuron->calcInput()));
        }
    }

    for (auto neuron : output) {
        neuron->setPower(normalize(neuron->calcInput()));
    }
}
