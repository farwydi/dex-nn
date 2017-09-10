#pragma once
#include "precompilation.h"

class Connect
{
public:
	Connect(Neuron *_base, Neuron *_way);
	~Connect();

	float echo(void);
	void learning(float E, float A);

private:
	float weight;
	float deltaWeight;

	Neuron *base;
	Neuron *way;
};