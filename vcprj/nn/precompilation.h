#pragma once

#include <string>
#include <vector>
#include <string>
#include <map>
#include <array>
#include <cmath>

class Connect;
class Neuron;
class Layout;
class HiddenLayout;
class InputLayout;
class ResultLayout;
class NeuralNetwork;

enum NeuronType
{
	INPUT,
	OUTPUT,
	HIDDEN
};

static const char *NeuronTypeStrings[] = { "INPUT", "OUTPUT", "HIDDEN" };

using namespace std;