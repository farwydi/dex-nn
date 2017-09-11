#pragma once

#include "precompilation.h"

class Neuron
{
public:
    Neuron(const NeuronType type, size_t countConnects, size_t countBacks, unsigned short id = 0,
           string levelPrefix = "");
    ~Neuron();

    void addConnect(Connect *to);
    void addBack(Neuron *to);

    void learning();
    NN_POINT calcInput();

    NN_POINT getDelta() const { return delta; }
    NN_POINT getPower() const { return power; }

    void setPower(NN_POINT x) { power = x; }
    void setDelta(NN_POINT x) { delta = x; }

    NN_POINT getBackPotential();
    NN_POINT getDirectionPotential(Neuron *to);

    char *name;

    // private:
    NN_POINT delta;
    NN_POINT power;

    vector<Connect *> connects;
    vector<Neuron *> backs;

    const NeuronType type;
};
