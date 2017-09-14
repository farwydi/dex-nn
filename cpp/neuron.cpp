#include "neuron.h"
#include "connect.h"

Neuron::Neuron(const NeuronType _type, size_t countConnects, size_t countBacks, unsigned short id,
               string levelPrefix)
    : type(_type)
{
    connects.reserve(countConnects);
    backs.reserve(countBacks);

    power = .0f;
    delta = .0f;

    auto _name = levelPrefix + string("_") + to_string(id);

    name = new char[_name.length() + 1];
    strcpy(name, _name.c_str());
}

Neuron::~Neuron() {}

vector<NN_POINT> Neuron::getWeights()
{
    vector<NN_POINT> result;

    for (auto connect : connects) {
        result.push_back(connect->getWeight());
    }

    return result;
}

void Neuron::restore(vector<NN_POINT> weights)
{
//    if (weights.count() != connects.count()) {
//        return; // error
//    }
//
//    for (int i = 0; i < connects.count(); i++) {
//        connects[i]->loadWeight(weights[i]);
//    }
}

void Neuron::addConnect(Connect *to)
{
    connects.push_back(to);
}

void Neuron::addBack(Neuron *to)
{
    backs.push_back(to);
}

NN_POINT Neuron::getBackPotential()
{
    NN_POINT potential = 0;
    for (auto back : backs) {
        potential += back->getDirectionPotential(this);
    }

    return potential;
}

NN_POINT Neuron::getDirectionPotential(Neuron *to)
{
    for (auto connect : connects) {
        if (connect->getWay() == to) {
            return delta * connect->getWeight();
        }
    }

    return 0;
}

void Neuron::learning()
{
    for (auto connect : connects) {
        connect->learning();
    }
}

NN_POINT Neuron::calcInput()
{
    NN_POINT r = 0;
    for (auto connect : connects) {
        r += connect->calcPotential();
    }

    return r;
}
