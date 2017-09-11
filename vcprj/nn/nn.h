#pragma once

#include "precompilation.h"

class NeuralNetwork
{
public:
    NeuralNetwork();
    ~NeuralNetwork();

    void set(array<float, INPUT_SIZE> params);

    array<float, OUTPUT_SIZE> result(bool _calc = true);

    void save();
    void load();

    array<float, OUTPUT_SIZE> mse(array<float, OUTPUT_SIZE> result,
                                  array<float, OUTPUT_SIZE> correct);

    array<float, OUTPUT_SIZE> learning(array<float, OUTPUT_SIZE> correct);

    // private:
    void calc();
    NN_POINT normalize(NN_POINT x);

    array<Neuron *, INPUT_SIZE> input;
    array<array<Neuron *, HIDDEN_SIZE>, HIDDEN_DEPTH> hidden;
    array<Neuron *, OUTPUT_SIZE> output;
};
