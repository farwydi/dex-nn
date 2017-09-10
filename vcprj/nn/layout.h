#pragma once

#include "precompilation.h"

class Layout
{
public:
	Layout(unsigned short size, const NeuronType _type, const string level = "");
	~Layout();

	void bind(Layout *layout);

	float f(float x);

	void process();

	void learning(float E, float A);

	vector<Neuron*> neurons;
};