#include "output.h"
#include "layout.h"
#include "hidden.h"
#include "neuron.h"

ResultLayout::ResultLayout(unsigned short _size, HiddenLayout *_hidden)
	: size(_size), hidden(_hidden)
{
	if (size > 0) {
		layout = new Layout(size, NeuronType::OUTPUT);

		layout->bind(*(hidden->layouts.end() - 1));
	}
}

ResultLayout::~ResultLayout()
{
}

float* ResultLayout::result()
{
	float *r = new float[size];

	layout->process();

	for (auto n = 0; n < size; n++) {
		r[n] = layout->neurons[n]->power;
	}

	return r;
}

void ResultLayout::learning(float *correct, size_t correctSize, float E, float A)
{
	if (correctSize != size) {
		return;
	}

	layout->process();

	for (auto n = 0; n < size; n++) {
		auto neuron = layout->neurons[n];

		neuron->delta = (correct[n] - neuron->power) * ((1 - neuron->power) * neuron->power);
	}

	hidden->calcDelta();

	for (auto neuron : layout->neurons) {
		neuron->learning(E, A);
	}
}
