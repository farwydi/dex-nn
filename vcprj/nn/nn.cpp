#include "nn.h"
#include "hidden.h"
#include "input.h"
#include "output.h"

NeuralNetwork::NeuralNetwork(unsigned short sizeInput, unsigned short sizeOutput, unsigned short sizeHidden, unsigned short depthHidden)
{
	hidden = new HiddenLayout(sizeHidden, depthHidden);
	input = new InputLayout(sizeInput, hidden);
	output = new ResultLayout(sizeOutput, hidden);

	E = .7f;
	A = .3f;
}

NeuralNetwork::~NeuralNetwork()
{
}

void NeuralNetwork::set(float * params, unsigned int paramsSize)
{
	if (paramsSize != input->size) {
		return;
	}

	for (unsigned int n = 0; n < paramsSize; n++) {
		input->set(n, params[n]);
	}
}

float * NeuralNetwork::result()
{
	hidden->calc();

	return output->result();
}

void NeuralNetwork::save()
{
}

void NeuralNetwork::load()
{
}

float * NeuralNetwork::mse(float * result, size_t resultSize, float * correct, size_t correctSize)
{
	if (resultSize != correctSize) {
		return nullptr;
	}

	float *mse = new float[resultSize];

	for (unsigned int n = 0; n < resultSize; n++) {
		mse[n] = pow(correct[n] - result[n], 2) / 1;
	}

	return mse;
}

void NeuralNetwork::setEA(float _E, float _A)
{
	E = _E;
	A = _A;
}

void NeuralNetwork::learning(float * correct, size_t correctSize)
{
	if (correctSize > output->size) {
		return; // error
	}

	hidden->calc();
	output->learning(correct, correctSize, E, A);
	hidden->learning(E, A);
	input->learning(E, A);
}
