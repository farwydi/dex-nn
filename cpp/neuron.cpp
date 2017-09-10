#include "neuron.h"
#include "connect.h"

Neuron::Neuron(const NeuronType _type, int id, const string levelPrefix)
	: type(_type)
{
	power = .0f;
	delta = .0f;
	name = NeuronTypeStrings[_type] + levelPrefix + '_' + to_string(id);
}

Neuron::~Neuron()
{
}

void Neuron::addConnect(Connect *to)
{
	connects.push_back(to);
}

void Neuron::addBack(Neuron *to)
{
	backs.push_back(to);
}

void Neuron::learning(float E, float A)
{
	for (auto connect : connects)
	{
		connect->learning(E, A);
	}
}

float Neuron::sum()
{
	float r = .0f;
	for (auto connect : connects)
	{
		r += connect->echo();
	}

	return r;
}