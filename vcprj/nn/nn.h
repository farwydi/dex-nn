#pragma once

#include "precompilation.h"

class NeuralNetwork
{
public:
	NeuralNetwork(unsigned short sizeInput, unsigned short sizeOutput, unsigned short sizeHidden, unsigned short depthHidden);
	~NeuralNetwork();

	void set(float *params, unsigned int paramsSize);

	float *result();

	void save();
	void load();

	float *mse(float *result, size_t resultSize, float *correct, size_t correctSize);

	void setEA(float E, float A);

	void learning(float *correct, size_t correctSize);

	HiddenLayout *hidden;
	ResultLayout *output;
	InputLayout *input;

	float E;
	float A;
};