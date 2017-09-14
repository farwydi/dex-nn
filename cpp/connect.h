#pragma once

#include "precompilation.h"

class Connect
{
public:
    Connect(Neuron *_base, Neuron *_way);
    ~Connect();

    NN_POINT calcPotential();
    void learning();

    void loadWeight(NN_POINT _weight) { weight = _weight; }

    NN_POINT getWeight() const { return weight; }
    Neuron *getWay() const { return way; }

private:
    NN_POINT weight;
    NN_POINT deltaWeight;

    Neuron *base;
    Neuron *way;
};
