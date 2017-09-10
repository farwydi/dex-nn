#pragma once
#include "precompilation.h"

class Neuron
{
public:
	Neuron(const NeuronType type, int id = 0, const string levelPrefix = "");
	~Neuron();

	void addConnect(Connect *to);
	void addBack(Neuron *to);

	void learning(float E, float A);
	float sum();

	float delta;
	float power;

	vector<Connect *> connects;
	vector<Neuron *> backs;
	
	NeuronType type;
	string name;
};