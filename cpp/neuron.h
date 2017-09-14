#pragma once

#include "precompilation.h"

class Neuron
{
public:
    Neuron(unsigned int countConnects, unsigned int countBacks);
    ~Neuron();

    void addConnect(Connect *to);
    void addBack(Neuron *to);

    void learning();
    NN_POINT calcInput();

    vector<NN_POINT> getWeights();
    void restore(vector<NN_POINT> weights);

    NN_POINT getDelta() const { return delta; }
    NN_POINT getPower() const { return power; }

    void setPower(NN_POINT x) { power = x; }
    void setDelta(NN_POINT x) { delta = x; }

    NN_POINT getBackPotential();
    NN_POINT getDirectionPotential(Neuron *to);

private:
    NN_POINT delta;
    NN_POINT power;

    vector<Connect *> connects;
    vector<Neuron *> backs;
};
