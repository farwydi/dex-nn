#include "connect.h"
#include "neuron.h"

void main()
{
	auto n = new Neuron(NeuronType::HIDDEN, 5, "_kek_LEVEL");
	auto m = new Neuron(NeuronType::HIDDEN, 5, "_kek_LEVEL");
	n->addConnect(new Connect(n, m));
}