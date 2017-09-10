#include "connect.h"
#include "neuron.h"

Connect::Connect(Neuron *_base, Neuron *_way)
    : base(_base), way(_way)
{
    deltaWeight = 0;
}

Connect::~Connect() {}

float Connect::echo(void)
{
    return way->power * weight;
}

void Connect::learning(float E, float A)
{
    float gradWeight = base->delta * way->power;

    deltaWeight = (E * gradWeight) + (A * deltaWeight);
    weight = weight + deltaWeight;
}