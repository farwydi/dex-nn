#pragma once

#include <array>
#include <cmath>
#include <map>
#include <string>
#include <cstring>
#include <vector>

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

// static const char *NeuronTypeStrings[] = {"INPUT", "OUTPUT", "HIDDEN"};

#define USE_LIMITER_CONNECTER 0

#if USE_LIMITER_CONNECTER == 1
#define COUNT_CONNECTS 3
#endif // USE_LIMITER_CONNECTER == 1

#define HIDDEN_DEPTH 1
#define HIDDEN_SIZE 3

#define INPUT_SIZE 2
#define OUTPUT_SIZE 1

#define LEARNING_TIME .15f
#define FORCE_ALPHA .3f

#define NN_POINT float

// #define USE_NORMALIZE_FUNC 0

using namespace std;
