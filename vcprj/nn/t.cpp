#include "connect.h"
#include "nn.h"
#include "input.h"
#include "output.h"
#include "layout.h"
#include "hidden.h"
#include "connect.h"
#include "neuron.h"

#include <iostream>

void mai1n()
{
	//// init
	auto __nn = new NeuralNetwork(2, 1, 2, 1);

	array<float, 2> sets;
	sets[0] = 1.f;
	sets[1] = .0f;
	__nn->set(sets.data(), 2);

	__nn->input->layout->neurons[0]->name = "I1";
	__nn->input->layout->neurons[1]->name = "I2";

	// h1 w1
	__nn->hidden->layouts[0]->neurons[0]->name = "H1";
	__nn->hidden->layouts[0]->neurons[0]->connects[0]->weight = 0.45f;
	__nn->hidden->layouts[0]->neurons[0]->connects[0]->name = "w1";
	// h1 w3
	__nn->hidden->layouts[0]->neurons[0]->connects[1]->weight = -0.12f;
	__nn->hidden->layouts[0]->neurons[0]->connects[1]->name = "w3";
	// h2 w2
	__nn->hidden->layouts[0]->neurons[1]->name = "H2";
	__nn->hidden->layouts[0]->neurons[1]->connects[0]->weight = 0.78f;
	__nn->hidden->layouts[0]->neurons[1]->connects[0]->name = "w2";
	// h2 w4
	__nn->hidden->layouts[0]->neurons[1]->connects[1]->weight = 0.13f;
	__nn->hidden->layouts[0]->neurons[1]->connects[1]->name = "w4";

	__nn->output->layout->neurons[0]->name = "O1";
	__nn->output->layout->neurons[0]->connects[0]->weight = 1.5f;
	__nn->output->layout->neurons[0]->connects[0]->name = "w5";
	__nn->output->layout->neurons[0]->connects[1]->weight = -2.3f;
	__nn->output->layout->neurons[0]->connects[1]->name = "w6";

	__nn->result();
	if (abs(__nn->output->layout->neurons[0]->power - 0.34f) < 0.0001f) {
		cout << "ERROR" << endl;
	}

	float *corrects = new float[1];
	corrects[0] = 1.f;
	__nn->learning(corrects, 1);

	__nn->result(); 

	if (abs(__nn->output->layout->neurons[0]->power - 0.37f) < 0.0001f) {
		cout << "ERROR" << endl;
	}

	cout << "TEST done" << endl;

	system("PAUSE");
}