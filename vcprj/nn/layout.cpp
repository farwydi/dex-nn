#include "layout.h"
#include "neuron.h"
#include "connect.h"

Layout::Layout(unsigned short size, const NeuronType _type, string level)
{
	unsigned short idx = 0;

	for (auto n = 0; n < size; n++) {
		neurons.push_back(new Neuron(_type, idx++, level));
	}
}

Layout::~Layout()
{
}

void Layout::bind(Layout *layout)
{
	for (auto base : neurons) {
		for (auto way : layout->neurons) {
			auto connect = new Connect(base, way);
			base->addConnect(connect);
			way->addBack(base);
		}
	}
}

float Layout::f(float x)
{
	return 1 / (1 + exp(-1 * x));
	// return (exp(-1 * 2 * x) - 1) / (exp(-1 * 2 * x) + 1);
}

void Layout::process()
{
	for (auto neuron : neurons) {
		float sum = neuron->sum();
		neuron->power = f(sum);
	}
}

void Layout::learning(float E, float A)
{
	for (auto neuron : neurons) {
		neuron->learning(E, A);
	}
}
