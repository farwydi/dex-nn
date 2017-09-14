#include "connect.h"
#include "neuron.h"

Connect::Connect(Neuron *_base, Neuron *_way) : base(_base), way(_way)
{
    deltaWeight = .0f;
    weight = static_cast<NN_POINT>(rand()) / static_cast<NN_POINT>(RAND_MAX);
}

Connect::~Connect()
{
}

NN_POINT Connect::calcPotential()
{
    return way->getPower() * weight;
}

void Connect::learning()
{
    NN_POINT gradWeight = base->getDelta() * way->getPower();

    deltaWeight = (LEARNING_TIME * gradWeight) + (FORCE_ALPHA * deltaWeight);
    weight = weight + deltaWeight;
}
