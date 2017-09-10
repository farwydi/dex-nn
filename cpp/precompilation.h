#pragma once

#include "iostream"

#include "vector"
#include "string"

class Connect;
class Neuron;

enum NeuronType
{
	INPUT,
	OUTPUT,
	HIDDEN
};

static const char *NeuronTypeStrings[] = { "INPUT", "OUTPUT", "HIDDEN" };

using namespace std;