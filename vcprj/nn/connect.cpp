#include "connect.h"
#include "neuron.h"

Connect::Connect(Neuron *_base, Neuron *_way)
    : base(_base), way(_way)
{
    deltaWeight = .0f;
	weight = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);

	name = "CONNECT_" + base->name + "_TO_" + way->name;
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