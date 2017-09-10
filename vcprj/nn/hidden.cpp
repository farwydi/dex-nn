#include "hidden.h"
#include "layout.h"
#include "neuron.h"
#include "connect.h"

HiddenLayout::HiddenLayout(unsigned short _size, unsigned short _depth)
	: size(_size), depth(_depth)
{
	for (auto d = 0; d < depth; d++) {
		auto layout = new Layout(size, NeuronType::HIDDEN, "_LEVEL_" + to_string(d));

		layouts.push_back(layout);

		if (d > 0) {
			layouts[d - 1]->bind(layout);
		}
	}
}

HiddenLayout::~HiddenLayout()
{
}

void HiddenLayout::learning(float E, float A)
{
	for (auto layout : layouts) {
		layout->learning(E, A);
	}
}

void HiddenLayout::calcDelta()
{
	calc();

	for (auto layout : layouts) {
		for (auto neuron : layout->neurons) {
			float delta = .0f;

			for (auto neuronBack : neuron->backs) {
				float weight = .0f;

				for (auto connect : neuronBack->connects) {
					if (connect->way == neuron) {
						weight = connect->weight;
						break;
					}
				}

				delta += neuronBack->delta * weight;
			}

			neuron->delta = ((1 - neuron->power) * neuron->power) * delta;
		}
	}
}

void HiddenLayout::calc()
{
	for (auto layout : layouts) {
		layout->process();
	}
}
